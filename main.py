#!/usr/bin/env python
import newrelic.agent
newrelic.agent.initialize('newrelic.ini')

import os
import sys
import tornado
import tornado.web
import tornado.wsgi
import tornado.ioloop
import tornado.options
import tornado.template
import tornado.httpserver

sys.argv.append('--logging=INFO')
tornado.options.parse_command_line()


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(template_name='home.html')


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
    (r"/api/", GitHubStream),
], **settings)


def main():
    http_server = tornado.httpserver.HTTPServer(
        tornado.wsgi.WSGIContainer(application))
    http_server.listen(os.environ.get('PORT', 8888))
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
