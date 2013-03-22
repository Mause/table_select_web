import json

# import tornado
import tornado.web
# import tornado.wsgi
# import tornado.ioloop
# import tornado.options
# import tornado.template
# import tornado.httpserver

# application specific
import db


class TablesHandler(tornado.web.RequestHandler):
    def get(self):
        "get is simple"
        self.session = db.Session()
        tables = db.get_tables(self.session)
        tables = json.dumps(tables)
        self.write(tables)

    def post(self):
        "post is hard"
        pass


class RemoveAttendeeHandler(tornado.web.RequestHandler):
    def get(self):
        pass
