import json
import logging
from contextlib import closing
from utils import (
    # BaseHandler,
    dict_from_query,
    # pluralize,
    singularize
)


class BaseRESTEndpoint(object):
    """
    A base generic handler for the Ember DATA RESTAdapter

    set the table to the declarative

    """

    table = None
    ember_model_name = None

    allowed_methods = None
    needs_admin = False

    Session = None

    def check_setup(self, method):
        # ensure that we have enabled the <method> method
        if method not in self.allowed_methods:
            self.set_bad_error(405)

        if self.needs_admin and not self.is_admin():
            self.set_status(401)
            return {
                'errors': [
                    {
                        'machine': 'authentication_invalid',
                        'human': 'You are not authorized'
                    }
                ]
            }

        # check we've been setup correctly
        assert self.table is not None, 'Bad table name'
        assert self.ember_model_name is not None, 'Bad EmberJS model name'

    def get(self):
        errors = self.check_setup('GET')
        if errors:
            self.write(json.dumps(errors, indent=4))
            return

        # parse the conditions
        conditions = self.build_conditions_from_args(
            self.request.arguments, self.table)

        with closing(self.Session()) as session:
            query = session.query(self.table.__table__)

            # import code
            # code.interact(local=locals())

            if conditions:
                logging.debug('{} filter conditions: {}'.format(
                    self.table.__tablename__,
                    conditions))
                query = query.filter_by(**conditions)

            records = dict_from_query(query.all())

            id_field_name = self.table.__tablename__ + '_id'

            for record in records:
                if id_field_name in record:
                    record['id'] = record[id_field_name]
                    del record[id_field_name]

            response = {
                self.ember_model_name: records
            }

            self.write(json.dumps(response, indent=4))

    def post(self):
        # check the setup
        self.check_setup('POST')

        # load in the filters
        body = self.decode_and_load(self.request.body)

        response = {}

        singular_model_name = singularize(self.ember_model_name)

        record_data = body[singular_model_name]

        with closing(self.Session()) as session:
            errors = self.perform_checks(session, record_data)

            if errors:
                response['errors'] = errors
            else:
                record_insert = self.table.__table__.insert(
                    record_data)

                session.execute(record_insert)
                session.commit()

                logging.info(
                    'added {} {}to db'.format(
                    singular_model_name, record_data))

                self.set_status(201)  # created

        self.write(json.dumps(response, indent=4))

    def build_conditions_from_args(self, args, table):
        try:
            conditions = {}
            for key, val in args.items():
                if val and key in table.__table__.columns.keys():
                    conditions[key] = val[0].decode('utf-8')
                else:
                    if not val:
                        logging.debug('Bad value; {}'.format(val))
                    else:
                        logging.debug('Bad filter')

                    self.set_bad_error(400)

        except UnicodeDecodeError:
            logging.debug('UnicodeDecodeError when decoding filters')
            self.set_bad_error(400)

        return conditions

    def decode_and_load(self, body):
        try:
            body = body.decode('utf-8')
        except UnicodeDecodeError:
            logging.debug('UnicodeDecodeError when decoding fields')
            self.set_bad_error(400)

        try:
            body = json.loads(body)
        except ValueError:
            logging.debug('ValueError when loading fields')
            self.set_bad_error(400)

        return body

    def perform_checks(self, session, record):
        for check in self.checks:
            errors = check(self, session, record)
            logging.debug('{}({}) -> {}'.format(
                check.__name__,
                record,
                errors))

            if errors:
                return errors

        return None
