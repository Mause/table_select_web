#!/usr/bin/env python3

# stdlib
import os
import sys
import logging

# setup newrelic
if 'HEROKU' in os.environ:
    import newrelic.agent
    newrelic.agent.initialize('newrelic.ini')

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
from includes import JS_INCLUDES
from settings import settings
from utils import BaseHandler, SmartStaticFileHandler

sys.argv.append('--logging=DEBUG')
tornado.options.parse_command_line()


# simple & dumb renderers; nothing fancy here
class MainHandler(BaseHandler):
    def get(self):
        self.render(
            'templates.html',
            path='/',
            js_includes=self.js_includes(JS_INCLUDES))

    def js_includes(self, listing):
        output = []
        for filename in listing:
            filename = self.static_url(filename)
            output.append('<script src="{}"></script>'.format(filename))
        return '\n'.join(output)


class TemplateHandler(BaseHandler):
    def get(self):
        logging.debug('Recompiled templates')
        args = ensure_templates(force=True)
        template = (
            'in_dir: {in_dir}<br/>'
            'out_file: {out_file}<br/>')
        self.write(template.format(**args))


def ensure_templates(force=False):
    out_file = os.path.join(
        os.path.dirname(__name__),
        'templates/templates.html')

    if not os.path.exists(out_file) or force:
        # not ideal, but w/e
        raw_template_dir = os.path.join(
            os.path.dirname(__file__),
            'static/templates')

        args = {
            'in_dir': raw_template_dir,
            'out_file': out_file
        }

        from static.templates.compact import compact
        compact(**args)

        return args


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


def get_ip():
    # import socket

    # ip = socket.gethostbyname(socket.gethostname())
    # ip = socket.gethostbyname(socket.getfqdn())
    # s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # s.connect(("gmail.com", 80))
    # ip = s.getsockname()[0]
    # s.close()

    # return ip
    return ''


tornado_settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "template_path": os.path.join(os.path.dirname(__file__), 'templates'),
    'cookie_secret': settings['cookie_secret'],
    "debug": True,
    "gzip": True,
}

application = tornado.web.Application(
    [
        (r'/static/(.*)', SmartStaticFileHandler,
            {'path': tornado_settings['static_path']}),

        # get only for ball table's
        (r"/api/v1/ball_tables(?:/(?P<record_id>\d+))?", ajax.BallTablesHandler),

        # this will be update, i suppose
        (r"/api/v1/removal_requests(?:/(?P<record_id>\d+))?", ajax.RemovalRequestHandler),

        # post! (and maybe get for some reason)
        (r"/api/v1/attendees(?:/(?P<record_id>\d+))?", ajax.AttendeeHandler),

        # (r"/api/v1/attendee/(?P<action>deny|allow)_bulk", ajax.ActionHandler),

        # (r"/admin", admin.AdminHandler),
        (r"/auth", admin.AuthHandler),
        (r"/logout", admin.LogoutHandler),
        (r"/templates", TemplateHandler),
        (r"/.*", MainHandler),
    ],
    **tornado_settings
)


def main():

    global Session, conn

    ensure_templates()
    Session, conn = setup_db()

    port = os.environ.get('PORT', 8888)
    addr = get_ip()
    print('{}:{}'.format(addr, port))

    try:
        application.listen(port)
        tornado.ioloop.IOLoop.instance().start()
    finally:
        conn.close()

if __name__ == '__main__':
    main()
