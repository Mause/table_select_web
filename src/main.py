#!/usr/bin/env python3

# stdlib
import os
import sys
import logging

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
from assets import gen_assets
from settings import settings, flags

# set the debug level for tornado
sys.argv.append('--logging=DEBUG')
tornado.options.parse_command_line()

# setup newrelic
if flags.is_production():
    import newrelic.agent

    if 'STAGING' in os.environ:
        environment = 'staging'
    else:
        environment = 'production'

    path = os.path.join(os.path.dirname(__file__), 'newrelic.ini')

    logging.debug("Initializing New Relic client...")
    newrelic.agent.initialize(path, environment=environment)


# only regen assets on each load when not in production mode... :P
if flags.is_production():
    ASSETS = gen_assets()
else:
    ASSETS = None


# simple & dumb renderer; nothing fancy here
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        newrelic_header = (
            newrelic.agent.get_browser_timing_header() if flags.is_production()
            else ''
        )
        self.render(
            'base.html',
            path='/',
            assets=ASSETS or gen_assets(),
            newrelic_header=newrelic_header)


def setup_db():
    from sqlalchemy import create_engine

    db_url = settings.get('DATABASE_URL')

    logging.debug('Database url is: {}'.format(db_url))

    engine = create_engine(db_url)
    engine.echo = False

    db.Base.metadata.create_all(engine)

    db.Session.configure(bind=engine)

    conn = engine.connect()

    return db.Session, conn


def get_ip():
    import socket

    ip = socket.gethostbyname(socket.gethostname())
    ip = socket.gethostbyname(socket.getfqdn())
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("gmail.com", 80))
    ip = s.getsockname()[0]
    s.close()

    return ip
    # return ''


tornado_settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "template_path": os.path.join(os.path.dirname(__file__), 'templates'),
    'cookie_secret': settings['cookie_secret'],
    "debug": settings['release'].upper() != "PRODUCTION",
    "gzip": True,
}

application = tornado.web.Application(
    [
        (r'/static/(.*)', tornado.web.StaticFileHandler,
            {'path': tornado_settings['static_path']}),

        (r"/api/v1/ball_tables(?:/(?P<record_id>\d+))?", ajax.BallTablesHandler),

        (r"/api/v1/removal_requests(?:/(?P<record_id>\d+))?", ajax.RemovalRequestHandler),

        (r"/api/v1/attendees(?:/(?P<record_id>\d+))?", ajax.AttendeeHandler),

        (r"/api/v1/me", ajax.AuthHandler),

        (r"/.*", MainHandler),
    ],
    **tornado_settings
)


def main():

    global Session, conn

    Session, conn = setup_db()

    addr = get_ip()
    port = os.environ.get('PORT', 8888)
    logging.debug('Running in {} mode, on {}:{}'.format(
        settings['release'],
        addr, port))

    try:
        application.listen(port)
        tornado.ioloop.IOLoop.instance().start()
    finally:
        conn.close()

if __name__ == '__main__':
    main()
