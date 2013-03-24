#!/usr/bin/env python
# import newrelic.agent
# newrelic.agent.initialize('newrelic.ini')

# stdlib
import os
import sys
# import logging
from contextlib import closing

# third party
import tornado
import tornado.web
import tornado.wsgi
import tornado.ioloop
import tornado.options
import tornado.template
import tornado.httpserver

# application specific
import ajax
import db
from utils import BaseHandler

sys.argv.append('--logging=INFO')
tornado.options.parse_command_line()


class MainHandler(BaseHandler):
    def get(self):
        self.render('home.html', path='/')


class InfoHandler(BaseHandler):
    def get(self):
        self.render('info.html', path='/info')


class AdminHandler(BaseHandler):
    def get(self):
        "this page will allow the authorization of removals"
        fields = ['request_id', 'attendee_id', 'table_id', 'remover_ident']
        with closing(db.Session()) as session:
            # keep removals persistant, for future reference
            # give every user a UUID, stored as a cookie,
            # that can be used to group requests
            query = (
                session.query(db.removal_request_table)
                    .filter_by(state='unresolved')
                    .all())

            query = [dict(zip(fields, record)) for record in query]
            # logging.info(query)

        self.render('admin.html', path='/admin', requests=query)


settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "template_path": os.path.join(os.path.dirname(__file__), 'templates'),
    "debug": True,
}


application = tornado.wsgi.WSGIApplication([
    (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': settings['static_path']}),
    (r"/api/tables", ajax.TablesHandler),
    (r"/api/attendee/remove", ajax.RemoveAttendeeHandler),
    (r"/api/attendee/add", ajax.AddAttendeeHandler),
    (r"/api/admin/attendee/(?P<action>deny|allow)_bulk", ajax.ActionHandler),
    (r"/admin", AdminHandler),
    (r"/info", InfoHandler),
    (r"/", MainHandler),
], **settings)


def main():
    http_server = tornado.httpserver.HTTPServer(
        tornado.wsgi.WSGIContainer(application))
    http_server.listen(os.environ.get('PORT', 8888))
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
