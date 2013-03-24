# stdlib
import json
import logging
from contextlib import closing

import tornado.web

# application specific
import db


class TablesHandler(tornado.web.RequestHandler):
    def get(self):
        "get is simple"
        with closing(db.Session()) as session:
            tables = db.get_tables(session)
            tables = json.dumps(tables, indent=4)
            self.write(tables)


class RemoveAttendeeHandler(tornado.web.RequestHandler):
    def post(self):
        attendee_id = self.get_argument('attendee_id')
        table_id = self.get_argument('table_id')

        logging.info(
            'recording removal request for attendee with id {}'.format(
                attendee_id))

        record = {
            'attendee_id': int(attendee_id),
            'table_id': int(table_id)
        }

        removal_request_insert = db.removal_request_table.insert()
        removal_request_insert.execute(record)


class AddAttendeeHandler(tornado.web.RequestHandler):
    def post(self):
        status = {"success": True}

        with closing(db.Session()) as session:
            attendee_name = self.get_argument('attendee_name')

            exists = db.does_attendee_exist(session, attendee_name)
            if exists:
                logging.info('attendee_exists: "{}"=="{}", on table {}'.format(
                    attendee_name, exists['attendee_name'],
                    exists['table_id']))
                status['error'] = 'attendee_exists'
                status['human_error'] = 'attendee already on {}'.format(
                    exists['table_id'])
                status['success'] = False

            else:
                table_id = self.get_argument('table_id')

                record = {
                    'attendee_name': attendee_name,
                    'table_id': int(table_id)
                }

                attendee_insert = db.attendee_table.insert()
                attendee_insert.execute(record)

                logging.info('attendee "{}" was added to table {}'.format(
                    attendee_name, table_id))

        self.write(json.dumps(status))

