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
import db
import ajax

sys.argv.append('--logging=INFO')
tornado.options.parse_command_line()


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        with closing(db.Session()) as self.session:
            tables = db.get_tables(self.session)
            self.render(template_name='home.html', tables=tables)


class GithubButtonHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('github-btn.html')


class GitHubStream(tornado.web.RequestHandler):
    def get(self):
        self.render('github_stream.html')


class AdminHandler(tornado.web.RequestHandler):
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
    (r"/", MainHandler),
], **settings)


def main():
    http_server = tornado.httpserver.HTTPServer(
        tornado.wsgi.WSGIContainer(application))
    http_server.listen(os.environ.get('PORT', 8888))
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
