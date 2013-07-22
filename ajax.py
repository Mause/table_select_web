# stdlib
import json
import logging
from contextlib import closing

# third party
import tornado

# application specific
import db
from settings import settings
from ember_data import BaseRESTEndpoint
from utils import BaseHandler, dict_from_query


class TornadoWebInterface(BaseHandler):
    def set_bad_error(self, status_code):
        raise tornado.web.HTTPError(status_code)

    def set_status(self, *args, **kwargs):
        super(TornadoWebInterface, self).set_status(*args, **kwargs)


class EmberDataRESTEndpoint(BaseRESTEndpoint, TornadoWebInterface):
    Session = db.Session
    pass


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

    allowed_methods = ['GET', 'POST']
    needs_admin = {
        'GET': False,
        'POST': False
    }

    # def post(self):
    #     attendee_id = self.get_argument('attendee_id')
    #     table_id = self.get_argument('table_id')

    #     logging.info(
    #         'recording removal request for attendee with id {}'.format(
    #             attendee_id))

    #     record = {
    #         'attendee_id': int(attendee_id),
    #         'table_id': int(table_id),
    #         'state': 'unresolved'
    #     }

    #     with closing(db.Session()) as session:
    #         record = db.removal_request_table.insert(record)
    #         session.execute(record)


class AttendeeHandler(EmberDataRESTEndpoint):
    table = db.Attendee
    ember_model_name = 'attendees'
    needs_admin = {
        'GET': False,
        'POST': False
    }

    allowed_methods = ['GET', 'POST']

    def check_record(self, attendee):
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

        attendees = dict_from_query(query.all())

        # check if the table is full
        return len(attendees) >= settings.get('max_pax_per_table', 10)

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


class ActionHandler(BaseHandler):
    def post(self, action):

        if action not in ['deny', 'allow']:
            return

        request_ids = self.request.body.decode('utf-8')
        request_ids = json.loads(request_ids)

        logging.info('{}ing {} request(s)'.format(action, len(request_ids)))

        if not request_ids:
            return

        with closing(db.Session()) as session:
            removal_request_condition = (
                db.removal_request_table.columns.request_id.in_(request_ids))

            # grab the current data
            removal_request_update = (
                session.query(db.removal_request_table)
                       .filter(removal_request_condition))

            # update the db with the new state
            removal_request_update.update(
                {db.removal_request_table.columns.state: action},
                synchronize_session=False
            )

            if action == "allow":
                # if we're allowing the removal request

                condition = (
                    db.attendee_table.columns.attendee_id ==
                    db.removal_request_table.columns.attendee_id)

                # grab the attendee record in question
                query = session.query(db.attendee_table)
                query = query.filter(condition)
                query = query.filter(removal_request_condition)

                to_update = dict_from_query(query.all())
                to_update = [attendee['attendee_id'] for attendee in to_update]

                query = session.query(db.attendee_table)
                query = query.filter(
                    db.attendee_table.columns.attendee_id.in_(to_update))

                query.update(
                    {db.attendee_table.columns.show: False},
                    synchronize_session=False
                )

            session.commit()
