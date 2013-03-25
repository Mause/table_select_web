
import tornado.web
# import os
import json
# import urllib
import logging
# import requests

# if 'HEROKU' not in os.environ:
#     # authentication data
#     with open('auth_data.json', 'r') as fh:
#         auth_data = json.loads(fh.read())
#         client_auth_data = auth_data["client_auth_data"]
# else:
#     client_auth_data = {}
#     client_auth_data['client_id'] = os.environ['CLIENT_ID']
#     client_auth_data['client_secret'] = os.environ['CLIENT_SECRET']


# def authed_fetch(url, headers={}):
#     headers.update({'X-Admin-Contact': 'me@mause.me'})
#     url += '?' + urllib.parse.urlencode(client_auth_data)
#     r = requests.get(url=url, headers=headers)
#     if 'x-ratelimit-remaining' in r.headers.keys():
#         logging.info('{} requests remaining for this hour.'.format(
#             r.headers['x-ratelimit-remaining']))
#     else:
#         logging.info('Request remaing for hour could not determined')
#         logging.info(r.content)
#     return r


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
