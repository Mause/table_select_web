# stdlib
import json

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
                if is_admin == True:
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
