import json
import logging
from functools import wraps
from contextlib import closing

from .authorised_endpoint import AuthorizedEndpoint

from utils import (
    dict_from_query,
    pluralize,
    singularize,
    get_primary_key_name_from_table
)


def check_setup_decorator(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        # check the setup
        errors = self.check_setup()
        if errors:
            self.write_json(errors)
            return

        return func(self, *args, **kwargs)

    return wrapper


class BaseRESTEndpoint(AuthorizedEndpoint):
    """
    A base generic handler for the Ember DATA RESTAdapter

    set 'table' to the declarative sqlalchemy table model defintion
    set 'ember_model_name' to the EmberJS model name
    set 'methods' to the allowed methods and their configuration;
        GET, POST, etc

    set 'Session' to a session creater created by the session_maker
    """

    table = None
    ember_model_name = None

    methods = {}
    Session = None
    json_indent = 4

    def check_setup(self):
        method = self.request.method

        # ensure that we have enabled the <method> method
        if method not in self.methods:
            self.set_bad_error(405)

        # check if you need to be an admin to access this method
        needs_admin = self.methods[method].get('needs_admin', False)
        if needs_admin and not self.is_authenticated():
            self.set_status(401)
            return {'errors': ['authentication_invalid']}

        # check we've been setup correctly
        assert self.table is not None, 'Bad table name'
        assert self.ember_model_name is not None, 'Bad EmberJS model name'

    @check_setup_decorator
    def get(self, record_id):
        response = {}

        # parse the conditions
        conditions = self.build_conditions_from_args(
            self.request.arguments, self.table)

        with closing(self.Session()) as session:
            query = session.query(self.table)

            records_key = self.ember_model_name

            if conditions and not record_id:
                logging.debug('{} conditions && ids: {}'.format(
                    self.table.__tablename__,
                    conditions))

                # apply the conditions
                query = self.apply_conditions(query, conditions)
                records = dict_from_query(query.all())

                records_key = pluralize(records_key)
                response[records_key] = records

            elif record_id:
                # we are returning a single record
                key = get_primary_key_name_from_table(self.table)
                key = getattr(self.table, key)
                query = query.filter(key == record_id)

                record = dict_from_query(query.one())
                records_key = singularize(records_key)
                response[records_key] = record

            self.write_json(response)

    @check_setup_decorator
    def post(self, record_id):
        if record_id is not None:
            raise NotImplementedError()

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
                record_key = singularize(self.ember_model_name)
                response[record_key] = dict_from_query(new_record)

                logging.info('added {} {} to db'.format(
                    self.table.__tablename__, record_data))

                # created HTTP status
                self.set_status(201)

        self.write_json(response)

    @check_setup_decorator
    def put(self, record_id):

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
                if not hasattr(record, key):
                    logging.warn(
                        'Patch of record of type {} attempted with unknown '
                        'field "{}"'.format(self.ember_model_name, key)
                    )
                    continue
                if getattr(record, key) != value:
                    # don't change anything unless we have to
                    # i'm not sure how the sqlalchmemy internals work,
                    # this might make for less work on the db interaction
                    setattr(record, key, value)

            session.add(record)
            session.commit()

            # update the frontends representation of the record with an id
            response[self.ember_model_name] = dict_from_query(record)

        self.write_json(response)

    def delete(self, record_id):
        raise NotImplementedError()

    def patch(self, record_id):
        raise NotImplementedError()

    def options(self, record_id):
        allowed = self.methods
        if record_id:
            if 'PUT' in allowed:
                del allowed['PUT']

        self.set_header('Allow', ', '.join(allowed.keys()))

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
            out['ids'] = decode(out['ids'])
            out['ids'] = list(map(int, out['ids']))
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
            if type(body) == bytes:
                body = body.decode('utf-8')

        except UnicodeDecodeError:
            logging.debug('UnicodeDecodeError whilst decoding fields')
            self.set_bad_error(400)

        if body == '':
            logging.debug('Bad JSON')
            self.set_bad_error(400)

        try:
            body = json.loads(body)
        except ValueError:
            logging.debug('ValueError whilst loading fields')
            self.set_bad_error(400)

        return body

    def perform_checks(self, session, record):
        checks = (getattr(self, item) for item in dir(self))
        checks = (
            item
            for item in checks
            if hasattr(item, '__record_checker__')
        )

        for check in checks:
            errors = check(session, record)
            logging.debug('{}({}) -> {}'.format(
                check.__name__,
                record,
                errors))

            if errors:
                return errors

        return None

    def write_json(self, data):
        self.set_header('Content-Type', 'application/json')
        return self.write(json.dumps(data, indent=self.json_indent))
