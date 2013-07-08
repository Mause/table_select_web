# stdlib
# import os
import json
# import logging
# import datetime
# import urllib.parse

# third-party
import tornado.web


def dict_from_query(query):
    dz = lambda d: dict(zip(d.keys(), d))

    if type(query) == list:
        return list(map(dz, query))
    else:
        return dz(query)


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
        kwargs.update(defaults)
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
