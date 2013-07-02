# stdlib
import json
import logging
from contextlib import closing

# application specific
import db
from utils import BaseHandler, dict_from_query
from settings import settings


# class TablesHandler(BaseHandler):
#     def get(self):
#         with closing(db.Session()) as session:
#             tables = db.get_tables(session)
#             self.write(json.dumps(tables, indent=4))


class BallTablesHandler(BaseHandler):
    def get(self):
        with closing(db.Session()) as session:
            tables = db.get_tables(session)

            # for table in tables:
                # if table['attendees']:
                #     ids = [
                #         attendee['attendee_id']
                #         for attendee in table['attendees']
                #         if attendee['show']]
                #     condition = (
                #         db.removal_request_table.columns.attendee_id.in_(
                #             set(ids)))
                #     query = session.query(db.removal_request_table).filter(
                #         condition).filter_by(state='unresolved')
                #     # .filter_by(show=True)
                #     query = dict_from_query(query.all())
                #     cur_states = {x['attendee_id']: x['state'] for x in query}

                #     for attendee in table['attendees']:
                #         if attendee['attendee_id'] in cur_states:
                #             attendee['state'] = 'submitted'
                #             attendee['removal_request_exists'] = True
                #         else:
                #             attendee['state'] = 'normal'
                #             attendee['removal_request_exists'] = False
            data = {
                'ball_tables': tables
            }
            # data = tables
            self.write(json.dumps(data, indent=4))


class RemovalRequestHandler(BaseHandler):
    def post(self):
        attendee_id = self.get_argument('attendee_id')
        table_id = self.get_argument('table_id')

        logging.info(
            'recording removal request for attendee with id {}'.format(
                attendee_id))

        record = {
            'attendee_id': int(attendee_id),
            'table_id': int(table_id),
            'state': 'unresolved'
        }

        removal_request_insert = db.removal_request_table.insert()
        removal_request_insert.execute(record)


class AddAttendeeHandler(BaseHandler):
    def post(self):
        # yikes this is complicated
        status = {"success": True}

        table_id = self.get_argument('table_id')
        attendee_name = self.get_argument('attendee_name')
        if not table_id or not attendee_name:
            self.error(400)
            status['success'] = False
            status['error'] = 'programming_error'
            status['human_error'] = 'An unknown error occured.'
        else:

            with closing(db.Session()) as session:

                # query the db for users on this table that can be shown
                query = (session.query(db.attendee_table)
                                .filter_by(table_id=table_id, show=True))

                attendees = dict_from_query(query.all())

                # check if the table is full
                if len(attendees) >= settings.get('max_pax_per_table', 10):
                    status['success'] = False
                    status['error'] = 'table_full'
                    status['human_error'] = (
                        "I'm sorry, that table is already full")
                else:
                    # check if the attendee is already on a table
                    exists = db.does_attendee_exist_smart(
                        session, attendee_name)
                    if exists:
                        logging.info(
                            'attendee_exists: "{}"=="{}", on table {}'.format(
                                attendee_name, exists['attendee_name'],
                                exists['table_id']))
                        status['error'] = 'attendee_exists'
                        status['human_error'] = (
                            'Attendee already on table {}'.format(
                                exists['table_id']))
                        status['success'] = False

                    else:

                        record = {
                            'attendee_name': attendee_name,
                            'table_id': int(table_id),
                            'show': True
                        }

                        logging.info(
                            'adding attendee "{}" to table {}'.format(
                            attendee_name, table_id))

                        attendee_insert = db.attendee_table.insert()
                        attendee_insert.execute(record)

        self.write(json.dumps(status, indent=4))


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
