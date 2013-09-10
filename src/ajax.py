# stdlib
import logging

# third party
import tornado

# application specific
import db
from settings import settings
from ember_data import BaseRESTEndpoint
from utils import BaseHandler


class TornadoWebInterface(BaseHandler):
    def set_bad_error(self, status_code):
        raise tornado.web.HTTPError(status_code)

    def set_status(self, *args, **kwargs):
        super(TornadoWebInterface, self).set_status(*args, **kwargs)


class EmberDataRESTEndpoint(BaseRESTEndpoint, TornadoWebInterface):
    Session = db.Session


class BallTablesHandler(EmberDataRESTEndpoint):
    table = db.BallTable
    ember_model_name = 'ball_tables'

    allowed_methods = ['GET']
    needs_admin = {
        'GET': False
    }


class RemovalRequestHandler(EmberDataRESTEndpoint):
    table = db.RemovalRequestTable
    ember_model_name = 'removal_request'

    allowed_methods = ['GET', 'POST', 'PUT']
    needs_admin = {
        'GET': True,
        'POST': False,
        'PUT': True
    }

    def check_ids(self, session, removal_request):
        logging.debug(removal_request)
        if removal_request['ball_table_id'] is None:
            logging.debug('Bad ball_table_id in posted removal_request')
            self.set_bad_error(400)
        elif removal_request['attendee_id'] is None:
            logging.debug('Bad attendee_id in posted removal_request')
            self.set_bad_error(400)

    checks = [
        check_ids
    ]


class AttendeeHandler(EmberDataRESTEndpoint):
    table = db.Attendee
    ember_model_name = 'attendees'
    needs_admin = {
        'GET': False,
        'POST': False,
        'PUT': False
    }

    allowed_methods = ['GET', 'POST', 'PUT']

    def check_record(self, session, attendee):
        if attendee['ball_table_id'] is None:
            self.set_bad_error(400)

    def check_if_table_full(self, session, attendee):

        if self.is_table_full(session, attendee['ball_table_id']):
            logging.info('table_full')
            errors = {
                'ball_table_id': [
                    {
                        'machine': 'table_full',
                        'human': 'That table is full'
                    }
                ]
            }
            self.set_status(400)
            return errors

        else:
            return {}

    def is_table_full(self, session, ball_table_id):

        # query the db for users on this table that can be shown
        query = session.query(db.Attendee)
        query = query.filter_by(ball_table_id=ball_table_id, show=True)

        num_attendees = query.count()

        # check if the table is full
        return num_attendees >= settings.get('max_pax_per_table', 10)

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
                'attendee_name': [
                    {
                        'machine': 'attendee_exists',
                        'human': 'Attendee "%@" already exists'
                    }
                ]
            }
            self.set_status(400)
            return errors
        else:
            return {}

    checks = [
        check_record,
        check_if_table_full,
        check_if_attendee_exists
    ]
