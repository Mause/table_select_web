# stdlib
import logging

# third party
import tornado

# application specific
import db
from settings import settings
from ember_data import BaseRESTEndpoint, record_check


class TornadoWebInterface(tornado.web.RequestHandler):
    def set_bad_error(self, status_code):
        raise tornado.web.HTTPError(status_code)

    def set_status(self, *args, **kwargs):
        super(TornadoWebInterface, self).set_status(*args, **kwargs)

    @property
    def headers(self):
        return self.request.headers


class EmberDataRESTEndpoint(BaseRESTEndpoint, TornadoWebInterface):
    Session = db.Session


class BallTablesHandler(EmberDataRESTEndpoint):
    table = db.BallTable
    ember_model_name = 'ball_tables'

    methods = {
        'GET': {
            'needs_auth': False
        },
        'PUT': {
            'needs_auth': False
        }
    }


class RemovalRequestHandler(EmberDataRESTEndpoint):
    table = db.RemovalRequestTable
    ember_model_name = 'removal_request'

    methods = {
        'GET': {
            'needs_auth': True
        },
        'POST': {
            'needs_auth': False
        },
        'PUT': {
            'needs_auth': True
        }
    }

    @record_check
    def check_ids(self, session, removal_request):
        logging.debug(removal_request)
        if removal_request['ball_table_id'] is None:
            logging.debug('Bad ball_table_id in posted removal_request')
            self.set_bad_error(400)
        elif removal_request['attendee_id'] is None:
            logging.debug('Bad attendee_id in posted removal_request')
            self.set_bad_error(400)
        else:
            return {}


class AttendeeHandler(EmberDataRESTEndpoint):
    table = db.Attendee
    ember_model_name = 'attendees'

    methods = {
        'GET': {
            'needs_admin': False
        },
        'POST': {
            'needs_admin': False
        },
        'PUT': {
            'needs_admin': False
        }
    }

    @record_check
    def check_record(self, session, attendee):
        if attendee['ball_table_id'] is None:
            self.set_bad_error(400)
        else:
            return {}

    @record_check
    def check_if_table_full(self, session, attendee):

        if self.is_table_full(session, attendee['ball_table_id']):
            logging.info('table_full')

            self.set_status(400)
            return {
                'ball_table_id': ['table_full']
            }

        else:
            return {}

    def is_table_full(self, session, ball_table_id):

        # query the db for users on this table that can be shown
        query = session.query(db.Attendee)
        query = query.filter_by(ball_table_id=ball_table_id, show=True)

        num_attendees = query.count()

        # check if the table is full
        return num_attendees >= settings.get('max_pax_per_table', 10)

    @record_check
    def check_if_attendee_exists(self, session, attendee):
        if settings.get('smart_attendee_name_check'):
            does_attendee_exist = db.does_attendee_exist_smart
        else:
            does_attendee_exist = db.does_attendee_exist_dumb

        attendee_name = attendee['attendee_name']

        # check if the attendee is already on a table
        if does_attendee_exist(session, attendee_name):
            logging.info('attendee_exists: "{}"'.format(
                         attendee_name))
            errors = {
                'attendee_name': ['attendee_exists']
            }
            self.set_status(400)
            return errors
        else:
            return {}


class AuthHandler(EmberDataRESTEndpoint):
    def post(self, record_id):
        # record_id is unused

        body = self.decode_and_load(self.request.body)

        if 'password' in body and 'username' in body and all(body.values()):
            username = body['username']
            password = body['password']

            auth_combos = settings.get('auth_combos', {})

            logging.info('supposed password was supplied; "{}"'.format(
                password))

            if username in auth_combos and password == auth_combos[username]:
                access_token = self.create_key(username.encode('utf-8'))

                self.write_json({
                    'api_key': {
                        'access_token': access_token,
                        'user_id': username
                    }
                })
            else:
                self.set_status(401)

        else:
            self.set_bad_error(400)
