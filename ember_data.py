import json
import logging
from contextlib import closing
from utils import (
    dict_from_query,
    pluralize,
    singularize,
    get_primary_key_name_from_table
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
    checks = []
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

    def get(self, record_id):
        errors = self.check_setup()
        if errors:
            self.write(json.dumps(errors, indent=4))
            return

        response = {}
        # parse the conditions
        conditions = self.build_conditions_from_args(
            self.request.arguments, self.table)

        with closing(self.Session()) as session:
            query = session.query(self.table)

            records_key = self.ember_model_name

            if conditions and not record_id:
                logging.debug('{} filter conditions: {}'.format(
                    self.table.__tablename__,
                    conditions))

                # apply the conditions
                query = self.apply_conditions(query, conditions)
                records = dict_from_query(query.all())

                response[pluralize(records_key)] = records

            elif record_id:
                # we are returning a single record
                key = get_primary_key_name_from_table(self.table)
                key = getattr(self.table, key)
                query = query.filter(key == record_id)

                record = dict_from_query(query.one())
                response[singularize(records_key)] = record

            self.write(json.dumps(response, indent=4))

    def post(self, record_id):
        if record_id is not None:
            raise NotImplementedError()

        # check the setup
        errors = self.check_setup()
        if errors:
            self.write(json.dumps(errors, indent=4))
            return

        response = {}

        record_data = self.get_record_data(self.request.body)

        with closing(self.Session()) as session:
            # perform any specified checks
            errors = self.perform_checks(session, record_data)

            if errors:
                # report any errors
                response['errors'] = errors
            else:
                # create a new record using the data
                new_record = self.table(**record_data)

                # instruct the session to save the record
                session.add(new_record)
                session.flush()
                session.commit()

                # refresh the in memory record with its corresponding id
                session.refresh(new_record)

                # update the frontends representation of the record with an id
                response[self.ember_model_name] = dict_from_query(new_record)

                logging.info(
                    'added {} {} to db'.format(
                    self.table.__tablename__, record_data))

                self.set_status(201)  # created

        self.write(json.dumps(response, indent=4))

    def put(self, record_id):
        # check the setup
        errors = self.check_setup()
        if errors:
            self.write(json.dumps(errors, indent=4))
            return

        response = {}

        record_data = self.get_record_data(self.request.body)

        with closing(self.Session()) as session:
            # get the primary key for the table
            key = get_primary_key_name_from_table(self.table)

            # need to make it a dict so that the args come out right
            conditions = {
                key: record_id
            }

            # grab the record we are updating
            query = session.query(self.table)
            query = query.filter_by(**conditions)
            record = query.one()

            # make the changes
            for key, value in record_data.items():
                if getattr(record, key) != value:
                    # don't change anything unless we have to
                    # i'm not sure how the sqlalchmemy internals work,
                    # this might make for less work on the db interaction
                    setattr(record, key, value)

            session.add(record)

            session.commit()

        self.write(json.dumps(response, indent=4))

    def delete(self):
        raise NotImplementedError()

    def patch(self):
        raise NotImplementedError()

    def get_record_data(self, request_body):
        body = self.decode_and_load(request_body)

        # get the singular version of the model name
        singular_model_name = singularize(self.ember_model_name)

        record = body.get(singular_model_name)

        if record is None:
            self.set_bad_error(400)
        else:
            return record

    def build_conditions_from_args(self, args, table):
        def decode(x):
            if type(x) == list:
                return [decode(sub_val) for sub_val in x]
            else:
                return x.decode('utf-8')

        try:
            out = {
                'conditions': {},
                'ids': []
            }
            # iterate through the key value pairs
            for key, val in args.items():

                if key == 'ids[]':
                    out['ids'] = val
                    continue

                # check if the filter is valid for the table
                if key and key in table.__table__.columns.keys():
                    out['conditions'][key] = decode(val[0])
                else:
                    logging.debug('Bad filter: {}={}'.format(key, val))

                    self.set_bad_error(400)

        except UnicodeDecodeError:
            logging.debug('UnicodeDecodeError whilst decoding filters')
            self.set_bad_error(400)

        try:
            out['ids'] = [int(id) for id in decode(out['ids'])]
        except ValueError as e:
            logging.error(e)
            self.set_bad_error(400)

        return out

    def apply_conditions(self, query, conditions):
        if conditions['ids']:
            primary_key = get_primary_key_name_from_table(self.table)
            in_ = getattr(self.table, primary_key).in_
            query = query.filter(in_(conditions['ids']))

        query = query.filter_by(**conditions['conditions'])

        return query

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
