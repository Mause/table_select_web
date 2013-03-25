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
            'table_id': int(table_id),
            'state': 'unresolved'
        }

        removal_request_insert = db.removal_request_table.insert()
        removal_request_insert.execute(record)


class AddAttendeeHandler(tornado.web.RequestHandler):
    def post(self):
        status = {"success": True}

        with closing(db.Session()) as session:
            attendee_name = self.get_argument('attendee_name')

            exists = db.does_attendee_exist_smart(session, attendee_name)
            if exists:
                logging.info('attendee_exists: "{}"=="{}", on table {}'.format(
                    attendee_name, exists['attendee_name'],
                    exists['table_id']))
                status['error'] = 'attendee_exists'
                status['human_error'] = 'Attendee already on table {}'.format(
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


class ActionHandler(tornado.web.RequestHandler):
    def post(self, action, *args, **kwargs):
        # fields = [
        #     'request_id',
        #     'attendee_id',
        #     'table_id',
        #     'remover_ident',
        #     'state'
        # ]

        logging.info('action: {}'.format(action))
        if action not in ['deny', 'allow']:
            return

        request_ids = self.request.body.decode('utf-8')
        request_ids = json.loads(request_ids)
        logging.info('{} request_ids'.format(len(request_ids)))

        if request_ids:
            with closing(db.Session()) as session:
                # for request_id in request_ids:
                #     to_update = session.query(
                #         db.removal_request_table).filter_by(
                #         request_id=request_id)
                #     to_update = dict(zip(fields, to_update.all()[0]))

                #     logging.info('{}ing removal_request {}'.format(
                #         action, request_id))
                #     to_update['state'] = action
                #     logging.info(to_update)

                query = session.query(db.removal_request_table)
                logging.info(query)
                sel = db.removal_request_table.columns.request_id.in_(request_ids)
                logging.info(sel)
                query.filter(sel)
                logging.info(query)

                query.update(
                    {'state': action}, synchronize_session='fetch')
                    # logging.info(removal_request_update)
                    # logging.info(removal_request_update)
                    # removal_request_update.execute()
