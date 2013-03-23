import json
import logging
from contextlib import closing

# import tornado
import tornado.web
# import tornado.wsgi
# import tornado.ioloop
# import tornado.options
# import tornado.template
# import tornado.httpserver

# application specific
import db


class TablesHandler(tornado.web.RequestHandler):
    def get(self):
        "get is simple"
        with closing(db.Session()) as self.session:
            tables = db.get_tables(self.session)
            tables = json.dumps(tables, indent=4)
            self.write(tables)


class RemoveAttendeeHandler(tornado.web.RequestHandler):
    def get(self):
        pass


class AddAttendeeHandler(tornado.web.RequestHandler):
    def post(self):
        status = {"success": True}

        with closing(db.Session()) as self.session:
            attendee_name = self.get_argument('attendee_name')

            if db.does_attendee_exist(self.session, attendee_name):
                status['error'] = 'user_exists'
                status['success'] = False

            else:
                table_id = self.get_argument('table_id')

                record = {
                    'attendee_name': attendee_name,
                    'table_id': table_id
                }

                logging.info(record)

                attendee_insert = db.attendee_table.insert()
                attendee_insert.execute(record)

        self.write(json.dumps(status))
