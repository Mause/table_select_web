#!/usr/bin/env python
# import newrelic.agent
# newrelic.agent.initialize('newrelic.ini')

# stdlib
import os
import sys
# import json
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
from utils import BaseHandler

sys.argv.append('--logging=INFO')
tornado.options.parse_command_line()


class MainHandler(BaseHandler):
    def get(self):
        self.render('home.html', path='/')


class GithubButtonHandler(BaseHandler):
    def get(self):
        self.render('github-btn.html')


class InfoHandler(BaseHandler):
    def get(self):
        self.render('info.html', path='/info')


class AdminHandler(BaseHandler):
    def get(self):
        "this page will allow the authorization of removals"
        # keep removals persistant, for future reference
        # give every user a UUID, stored as a cookie,
        # that can be used to group requests


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
