import re
import json
import time
import hmac
import base64
import logging
from contextlib import closing

from settings import settings
from utils import (
    dict_from_query,
    pluralize,
    singularize,
    get_primary_key_name_from_table
)

SEP = str(base64.b64encode(b'DOM'))[2:-1]
AUTH_RE = re.compile(r'(\w+) (.*)')
API_KEY_SEED = settings['api_key_seed'].encode('utf-8') or b'bytes'


def record_check(func):
    func.__record_checker__ = True
    return func


class AuthorizedEndpoint(object):
    def is_authenticated(self):
        if 'Authorization' not in self.headers:
            logging.info('Attempted to access restricted endpoint without authentication')
            return False
        else:
            auth_data = self.headers['Authorization']
            match = AUTH_RE.match(auth_data)
            if match:
                auth_type = match.groups()[0]
                if auth_type == 'none':
                    logging.info('Attempted to access restricted endpoint with "none" authentication')
                    return False
                elif auth_type == 'Bearer':
                    key = match.groups()[1]

                    if self.verify_key(key):
                        return True
                    else:
                        logging.info('Attempted to access restricted endpoint with invalid authentication key')
                else:
                    self.set_bad_error(401)
            else:
                logging.info('Attempted to access restricted endpoint with invalid authentication')

    def verify_key(self, key):
        user_hash, timestamp = key.split(SEP)

        timestamp = base64.b64decode(timestamp.encode('utf-8'))
        timestamp = float(timestamp.decode('utf-8'))

        possible_users = {
            hmac.new(API_KEY_SEED, username.encode('utf-8')).hexdigest()
            for username in settings['auth_combos'].keys()
        }

        if timestamp > time.time():
            logging.info('Invalid key, timestamp in future')
            return False

        elif user_hash not in possible_users:
            logging.info('No such user hash')
            return False

        else:
            return True

    def create_key(self, username):
        user_hash = hmac.new(API_KEY_SEED, username).hexdigest()

        timestamp = str(base64.b64encode(str(time.time()).encode('utf-8')))[2:-1]

        ret = '{}{}{}'.format(
            user_hash,
            SEP,
            timestamp
        )
        if "b'" in ret:
            import code
            code.interact(local=locals())
        return ret


class BaseRESTEndpoint(AuthorizedEndpoint):
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
        'POST': False,
        'PUT': False
    }
    Session = None
    json_indent = 4

    def check_setup(self):
        method = self.request.method

        # ensure that we have enabled the <method> method
        if method not in self.allowed_methods:
            self.set_bad_error(405)

        # check if you need to be an admin to access this method
        if self.needs_admin[method] and not self.is_authenticated():
            self.set_status(401)
            return {'errors': ['authentication_invalid']}

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
                record_key = singularize(self.ember_model_name)
                response[record_key] = dict_from_query(new_record)

                logging.info('added {} {} to db'.format(
                    self.table.__tablename__, record_data))

                self.set_status(201)  # created

        self.write_json(response)

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

            # update the frontends representation of the record with an id
            response[self.ember_model_name] = dict_from_query(record)

        self.write_json(response)

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
