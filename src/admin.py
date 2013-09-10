import json
import logging

from settings import settings
from utils import BaseHandler


class AuthHandler(BaseHandler):
    def get(self):
        self.render('auth.html', path="/auth")

    def post(self):
        password = self.get_argument('password')
        username = self.get_argument('username')

        if password and username:
            auth_combos = settings.get('auth_combos', {})

            logging.info('supposed password was supplied; "{}"'.format(
                password))

            if username in auth_combos.keys():
                if password == auth_combos[username]:
                    self.set_secure_cookie('is_admin', json.dumps(True))
                    self.redirect('/admin')
                    return
                else:
                    self.redirect('/')
                    return
            else:
                self.redirect('/')
                return

        else:
            self.redirect('/')


class LogoutHandler(BaseHandler):
    def get(self):
        self.set_secure_cookie('is_admin', json.dumps(False))
        self.redirect('/')
