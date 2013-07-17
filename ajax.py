# stdlib
import json
import logging
from contextlib import closing

# third party
import tornado

# application specific
import db
from settings import settings
from utils import (
    BaseHandler,
    dict_from_query,
    pluralize  # ,
    # singularize
)


class EmberDataRESTEndpoint(BaseHandler):
    table = None
    ember_model_name = None

    allowed_methods = None
    needs_admin = False

    def check_setup(self, method):
        # ensure that we have enabled the <method> method
        if method not in self.allowed_methods:
            raise tornado.web.HTTPError(405)

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

        with closing(db.Session()) as session:
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

        singular_model_name = pluralize(self.ember_model_name)

        record_data = body[singular_model_name]

        with closing(db.Session()) as session:
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

                    raise tornado.web.HTTPError(400)

        except UnicodeDecodeError:
            logging.debug('UnicodeDecodeError when decoding filters')
            raise tornado.web.HTTPError(400)

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


class BallTablesHandler(EmberDataRESTEndpoint):
    table = db.BallTable
    ember_model_name = 'ball_tables'

    allowed_methods = ['GET']
    needs_admin = False


class RemovalRequestHandler(BaseHandler):
    table = db.RemovalRequestTable
    ember_model_name = 'removal_request'

    allowed_methods = ['GET']
    needs_admin = False

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
    table = db.AttendeeTable
    ember_model_name = 'attendees'
    needs_admin = False

    # dont allow anything, we want to roll our own this time
    allowed_methods = ['GET', 'POST']

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
        query = session.query(db.AttendeeTable.__table__)
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
