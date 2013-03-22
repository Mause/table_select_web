#!/usr/bin/env python
# import newrelic.agent
# newrelic.agent.initialize('newrelic.ini')

# stdlib
import os
import sys
import json
import logging
logging
json

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
        self.session = db.Session()

        tables = db.get_tables(self.session)

        self.render(template_name='home.html', tables=tables)


class GithubButtonHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('github-btn.html')


class GitHubStream(tornado.web.RequestHandler):
    def get(self):
        self.render('github_stream.html')

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "template_path": os.path.join(os.path.dirname(__file__), 'templates'),
    "debug": True,
}


application = tornado.wsgi.WSGIApplication([
    (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': settings['static_path']}),
    (r"/", MainHandler),
    (r"/api/tables", ajax.TablesHandler),
    (r"/api/attendee/remove", ajax.RemoveAttendeeHandler)
], **settings)


def main():
    http_server = tornado.httpserver.HTTPServer(
        tornado.wsgi.WSGIContainer(application))
    http_server.listen(os.environ.get('PORT', 8888))
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
