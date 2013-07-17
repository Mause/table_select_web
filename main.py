#!/usr/bin/env python

# stdlib
import os
import sys

# # setup newrelic
# if 'HEROKU' in os.environ:
#     import newrelic.agent
#     newrelic.agent.initialize('newrelic.ini')

# third party
import tornado
import tornado.web
import tornado.wsgi
import tornado.ioloop
import tornado.options
import tornado.httpserver

# application specific
import db
import ajax
import admin
from settings import settings
from utils import BaseHandler, SmartStaticFileHandler

sys.argv.append('--logging=DEBUG')
tornado.options.parse_command_line()


# simple & dumb renderers; nothing fancy here
class MainHandler(BaseHandler):
    def get(self):
        self.render('templates.html', path='/')

tornado_settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "template_path": os.path.join(os.path.dirname(__file__), 'templates'),
    'cookie_secret': settings['cookie_secret'],
    "debug": True,
}


application = tornado.wsgi.WSGIApplication(
    [
        (r'/static/(.*)', SmartStaticFileHandler,
            {'path': tornado_settings['static_path']}),

        # get only for ball table's
        (r"/api/v1/ball_tables", ajax.BallTablesHandler),

        # this will be update, i suppose
        (r"/api/v1/attendees/remove", ajax.RemovalRequestHandler),

        # post! (and maybe get for some reason)
        (r"/api/v1/attendees", ajax.AttendeeHandler),

        (r"/api/v1/attendee/(?P<action>deny|allow)_bulk", ajax.ActionHandler),

        (r"/admin", admin.AdminHandler),
        (r"/auth", admin.AuthHandler),
        (r"/logout", admin.LogoutHandler),
        (r"/.*", MainHandler),
    ],
    **tornado_settings
)


def ensure_templates():
    out_file = os.path.join(
        os.path.dirname(__name__),
        'templates',
        'templates.html')

    if not os.path.exists(out_file):
        # not ideal, but w/e
        raw_template_dir = os.path.join(
            os.path.dirname(__file__),
            'static',
            'templates')

        from static.templates.compact import compact
        compact(
            in_dir=raw_template_dir,
            out_file=out_file)


def setup_db():
    from sqlalchemy import create_engine

    default_url = settings.get('DATABASE_URL')
    db_url = os.environ.get("DATABASE_URL", default_url)

    engine = create_engine(db_url)
    engine.echo = False

    # db.metadata.create_all(engine)
    db.Base.metadata.create_all(engine)

    db.Session.configure(bind=engine)

    conn = engine.connect()

    return db.Session, conn


def main():

    global Session, conn

    ensure_templates()
    Session, conn = setup_db()

    try:
        http_server = tornado.httpserver.HTTPServer(
            tornado.wsgi.WSGIContainer(application))

        port = os.environ.get('PORT', 8888)
        print('PORT:', port)
        http_server.listen(port)
        # application.listen(port)
        tornado.ioloop.IOLoop.instance().start()
    finally:
        conn.close()

if __name__ == '__main__':
    main()
