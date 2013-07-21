import json
import logging
from contextlib import closing
from utils import (
    dict_from_query,
    # pluralize,
    singularize
)


class BaseRESTEndpoint(object):
    """
    A base generic handler for the Ember DATA RESTAdapter

    set 'table' to the declarative sqlalchemy table model defintion
    set 'ember_model_name' to the EmberJS model name
    set 'allowed_methods' to the allowed methods; GET, POST, etc
    set 'needs_admin' to a dict for methods that needs admin

    set 'Session' to a session creater created by the session_maker
    """

    table = None
    ember_model_name = None

    allowed_methods = None
    needs_admin = {
        'GET': False,
        'POST': False
    }
    Session = None

    def check_setup(self):
        method = self.request.method

        # ensure that we have enabled the <method> method
        if method not in self.allowed_methods:
            self.set_bad_error(405)

        # check if you need to be an admin to access this method
        if self.needs_admin[method] and not self.is_admin():
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
        errors = self.check_setup()
        if errors:
            self.write(json.dumps(errors, indent=4))
            return
        else:
            logging.debug('Setup is good')

        response = {}
        # parse the conditions
        conditions = self.build_conditions_from_args(
            self.request.arguments, self.table)

        # TODO: for later :P
        # requested_ids = self.get_arguments('ids[]')

        with closing(self.Session()) as session:
            query = session.query(self.table)

            if conditions:
                logging.debug('{} filter conditions: {}'.format(
                    self.table.__tablename__,
                    conditions))

                query = query.filter_by(**conditions)

            records = dict_from_query(query.all())

            response[self.ember_model_name] = records

            self.write(json.dumps(response, indent=4))

    def post(self):
        # check the setup
        errors = self.check_setup()
        if errors:
            self.write(json.dumps(errors, indent=4))
            return

        # load in the filters
        body = self.decode_and_load(self.request.body)

        response = {}

        # get the singular version of the model name
        singular_model_name = singularize(self.ember_model_name)

        # grab the new record data
        record_data = body[singular_model_name]

        with closing(self.Session()) as session:
            # perform any specified checks
            errors = self.perform_checks(session, record_data)

            if errors:
                # report any errors
                response['errors'] = errors
            else:
                # create a new record using the data
                new_record = self.table(**record_data)

                session.add(new_record)
                session.commit()

                logging.info(
                    'added {} {} to db'.format(
                    singular_model_name, record_data))

                self.set_status(201)  # created

        self.write(json.dumps(response, indent=4))

    def build_conditions_from_args(self, args, table):
        try:
            conditions = {}
            # iterate through the key value pairs
            for key, val in args.items():
                val = val[0].decode('utf-8')

                # check if the filter is valid for the table
                if key and key in table.__table__.columns.keys():
                    conditions[key] = val
                else:
                    logging.debug('Bad filter: {}={}'.format(key, val))

                    self.set_bad_error(400)

        except UnicodeDecodeError:
            logging.debug('UnicodeDecodeError whilst decoding filters')
            self.set_bad_error(400)

        return conditions

    def decode_and_load(self, body):
        try:
            body = body.decode('utf-8')
        except UnicodeDecodeError:
            logging.debug('UnicodeDecodeError whilst decoding fields')
            self.set_bad_error(400)

        try:
            body = json.loads(body)
        except ValueError:
            logging.debug('ValueError whilst loading fields')
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
