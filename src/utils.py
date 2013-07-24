# stdlib
# import os
import json
from settings import settings
# import logging
# import datetime
# import urllib.parse
from sqlalchemy.orm.collections import InstrumentedList
# from sqlalchemy.util import KeyedTuple

# third-party
import tornado.web


def pluralize(name):
    plurals = settings.get('plurals')

    if plurals and name in plurals:
        return plurals[name]
    else:
        if not name.endswith('s'):
            return name + "s"
        else:
            return name


# use the same plurals hash to determine
# special-case singularization
def singularize(name):
    plurals = settings.get('plurals')
    if plurals:
        for i in plurals.keys():
            if plurals[i] == name:
                return i

    if name.endswith('s'):
        return name[:-1]
    else:
        return name


# these functions assume that there is only one primary key
def get_primary_key_name_from_table(table):
    if hasattr(table, '__table__'):
        table = table.__table__
    assert len(table.primary_key.columns.keys()) < 2
    return table.primary_key.columns.keys()[0]


def get_primary_key_from_record(record):
    key = get_primary_key_name_from_table(record)
    return record.__dict__[key]


def dict_from_query(query, debug=False):
    def serialize(record, ids_only=False):
        if type(record) in (list, InstrumentedList):
            return [serialize(sub, ids_only=True) for sub in record]

        if ids_only:
            return get_primary_key_from_record(record)
        else:
            out = {}
            for key, value in record.items():
                if type(value) == InstrumentedList:
                    key = singularize(key) + '_ids'
                    value = serialize(value, ids_only=True)
                out[key] = value
            return out

    if type(query) == list:
        return list(map(serialize, query))
    else:
        return serialize(query)


class BaseHandler(tornado.web.RequestHandler):
    def is_admin(self):
        is_admin = self.get_secure_cookie('is_admin')
        self.admin_cookied_yes = False

        if is_admin:
            try:
                is_admin = json.loads(is_admin.decode('utf-8'))
            except ValueError:
                self.admin_cookied_yes = False
            else:
                if is_admin:
                    self.admin_cookied_yes = True
                else:
                    self.admin_cookied_yes = False

        return self.admin_cookied_yes

    def render(self, template_name, **kwargs):
        # we do it this way so that the handler can overwrite defaults :D
        defaults = {
            'commit_hash': None,
            'is_admin': self.is_admin()
        }
        args = defaults
        args.update(kwargs)
        return super(BaseHandler, self).render(template_name, **kwargs)


class SmartStaticFileHandler(tornado.web.StaticFileHandler):
    pass
    # def get_age(self, path):
    #     import stat
    #     abspath = os.path.abspath(path)
    #     stat_result = os.stat(abspath)
    #     modified = datetime.datetime.fromtimestamp(
    #         stat_result[stat.ST_MTIME])
    #     return modified

    # def get(self, path, include_body=True):
    #     orig_path = path

    #     filename = urllib.parse.urlparse(orig_path).path
    #     if filename.endswith('.hbs.js'):
    #         path = self.parse_url_path(path)
    #         abspath = os.path.abspath(os.path.join(self.root, path))

    #     else:
    #         super(SmartStaticFileHandler, self).get(orig_path, include_body)
