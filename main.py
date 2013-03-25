#!/usr/bin/env python

# stdlib
import os
import sys

if 'HEROKU' in os.environ:
    import newrelic.agent
    newrelic.agent.initialize('newrelic.ini')

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
import admin
from utils import BaseHandler
from settings import settings

sys.argv.append('--logging=INFO')
tornado.options.parse_command_line()


class MainHandler(BaseHandler):
    def get(self):
        self.render('home.html', path='/')


class InfoHandler(BaseHandler):
    def get(self):
        self.render('info.html', path='/info')


settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "template_path": os.path.join(os.path.dirname(__file__), 'templates'),
    "debug": True,
    'cookie_secret': settings['cookie_secret']
}


application = tornado.wsgi.WSGIApplication([
    (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': settings['static_path']}),
    (r"/api/tables", ajax.TablesHandler),
    (r"/api/attendee/remove", ajax.RemoveAttendeeHandler),
    (r"/api/attendee/add", ajax.AddAttendeeHandler),
    (r"/api/admin/attendee/(?P<action>deny|allow)_bulk", ajax.ActionHandler),
    (r"/admin", admin.AdminHandler),
    (r"/auth", admin.AuthHandler),
    (r"/logout", admin.LogoutHandler),
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
