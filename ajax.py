# stdlib
import json
import logging
from contextlib import closing

# application specific
import db
from utils import BaseHandler, dict_from_query
from settings import settings


class TablesHandler(BaseHandler):
    def get(self):
        "get is simple"
        with closing(db.Session()) as session:
            tables = db.get_tables(session)
            tables = json.dumps(tables, indent=4)
            self.write(tables)


class RemoveAttendeeHandler(BaseHandler):
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
        status = {"success": True}

        with closing(db.Session()) as session:
            table_id = self.get_argument('table_id')

            query = session.query(db.attendee_table).filter_by(
                    table_id=table_id, show=True)

            attendees = dict_from_query(query.all())

            if len(attendees) >= settings.get('max_pax_per_table', 10):
                status['success'] = False
                status['error'] = 'table_full'
                status['human_error'] = "I'm sorry, that table is already full"
            else:
                attendee_name = self.get_argument('attendee_name')

                exists = db.does_attendee_exist_smart(session, attendee_name)
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

        self.write(json.dumps(status))


class ActionHandler(BaseHandler):
    def post(self, action, *args, **kwargs):
        if action not in ['deny', 'allow']:
            return

        request_ids = self.request.body.decode('utf-8')
        request_ids = json.loads(request_ids)

        logging.info('{}ing {} request(s)'.format(action, len(request_ids)))

        if request_ids:
            with closing(db.Session()) as session:
                for request_id in request_ids:
                    removal_request_to_update = session.query(
                        db.removal_request_table).filter_by(
                        request_id=request_id)
                    removal_request_updated_data = dict_from_query(
                        removal_request_to_update.one())

                    removal_request_updated_data['state'] = action

                    removal_request_to_update.update(
                        removal_request_updated_data,
                        synchronize_session=False)
                    session.commit()

                    if action == "allow":
                        logging.info(
                            'allowing deletion of attendee with id {}'.format(
                                removal_request_updated_data['attendee_id']))

                        attendee_table_update = (
                            session.query(db.attendee_table).filter_by(
                                attendee_id=removal_request_updated_data[
                                'attendee_id']))

                        attendee_updated_data = dict_from_query(
                            attendee_table_update.one())

                        attendee_updated_data['show'] = False
                        logging.info(attendee_updated_data)

                        attendee_table_update.update(attendee_updated_data,
                            synchronize_session=False)
                        session.commit()
