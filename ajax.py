# stdlib
import json
import logging
from contextlib import closing

# third party
import tornado

# application specific
import db
from utils import BaseHandler, dict_from_query
from settings import settings


class EmberDataRESTEndpoint(BaseHandler):
    table = db.ball_table
    ember_model_name = None
    allowed_methods = []

    def get(self):
        if 'GET' not in self.allowed_methods:
            raise tornado.web.HTTPError(405)

        assert self.table is not None, 'Bad table name'
        assert self.ember_model_name is not None, 'Bad EmberJS model name'

        conditions = self.build_conditions_from_args(
            self.request.arguments, db.ball_table)

        with closing(db.Session()) as session:
            query = (session.query(self.table)
                            .filter_by(**conditions))

            records = dict_from_query(query.all())

            id_field_name = self.table.name + '_id'

            for record in records:
                if id_field_name in record:
                    record['id'] = record[id_field_name]
                    del record[id_field_name]

            data = {
                self.ember_model_name: records
            }

            self.write(json.dumps(data, indent=4))

    def build_conditions_from_args(self, args, table):
        try:
            conditions = {}
            for key, val in args.items():
                if val and key in table.columns.keys():
                    conditions[key] = val[0].decode('utf-8')
                else:
                    if not val:
                        logging.debug('Bad value; {}'.format(val))
                    else:
                        logging.debug('Bad filter')

                    raise tornado.web.HTTPError(400)

        except UnicodeDecodeError:
            logging.debug('UnicodeDecodeError when decoding filters')
            raise tornado.web.HTTPError(400)

        logging.debug('{} filter conditions: {}'.format(
            self.table.name,
            conditions))

        return conditions

    def decode_and_load(self, body):
        try:
            body = body.decode('utf-8')
        except UnicodeDecodeError:
            logging.debug('UnicodeDecodeError when decoding fields')
            raise tornado.web.HTTPError(400)

        try:
            body = json.loads(body)
        except ValueError:
            logging.debug('ValueError when loading fields')
            raise tornado.web.HTTPError(400)

        return body


class BallTablesHandler(EmberDataRESTEndpoint):
    table = db.ball_table
    ember_model_name = 'ball_tables'
    allowed_methods = ['GET']


class RemovalRequestHandler(BaseHandler):
    table = db.removal_request_table
    ember_model_name = 'removal_request'

    allowed_methods = ['GET']

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
    table = db.attendee_table
    ember_model_name = 'attendees'

    # dont allow anything, we want to roll our own this time
    allowed_methods = ['GET']

    def is_table_full(self, session, ball_table_id):
        # query the db for users on this table that can be shown
        query = (session.query(db.attendee_table)
                        .filter_by(ball_table_id=ball_table_id, show=True))

        attendees = dict_from_query(query.all())

        # check if the table is full
        return len(attendees) >= settings.get('max_pax_per_table', 10)

    def post(self):
        body = self.decode_and_load(self.request.body)

        # yikes this is complicated
        response = {}

        attendee = body['attendee']
        ball_table_id = attendee['ball_table_id']
        attendee_name = attendee['attendee_name']

        if settings.get('smart_attendee_name_check'):
            does_attendee_exist = db.does_attendee_exist_smart
        else:
            does_attendee_exist = db.does_attendee_exist_dumb

        with closing(db.Session()) as session:

            if self.is_table_full(session, ball_table_id):
                logging.info('table_full')
                response['errors'] = {
                    'ball_table_id': [
                        'table_full'
                    ]
                }
                self.set_status(400)

            elif does_attendee_exist(session, attendee_name):
                # check if the attendee is already on a table
                logging.info('attendee_exists: "{}"'.format(
                             attendee_name))
                response['errors'] = {
                    'attendee_name': [
                        'attendee_exists'
                    ]
                }
                self.set_status(400)
            else:

                record = {
                    'attendee_name': attendee_name,
                    'ball_table_id': ball_table_id,
                    'show': True
                }

                attendee_insert = db.attendee_table.insert(record)
                session.execute(attendee_insert)
                session.commit()

                logging.info(
                    'added attendee "{}" to table {}'.format(
                    attendee_name, ball_table_id))

                # response['attendee'] = record  # do we return the record?

                self.set_status(201)  # created

        self.write(json.dumps(response, indent=4))


class ActionHandler(BaseHandler):
    def post(self, action):
        if not self.is_admin():
            return

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
                attendee_table_update = (
                    session.query(db.attendee_table)
                           .filter(condition)
                           .filter(removal_request_condition)
                )

                to_update = dict_from_query(attendee_table_update.all())
                to_update = [attendee['attendee_id'] for attendee in to_update]

                attendee_table_update = (
                    session.query(db.attendee_table)
                           .filter(db.attendee_table.columns.attendee_id.in_(to_update)))

                attendee_table_update.update(
                    {db.attendee_table.columns.show: False},
                    synchronize_session=False
                )

            session.commit()
