import logging
import json
from contextlib import closing

import db
from settings import settings
from utils import BaseHandler, dict_from_query


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


class AdminHandler(BaseHandler):
    def get(self):
        "this page will allow the authorization of removals"
        if self.is_admin():

            with closing(db.Session()) as session:
                # keep removals persistant, for future reference
                # give every user a UUID, stored as a cookie,
                # that can be used to group requests
                query = (session.query(db.removal_request_table)
                                .filter_by(state='unresolved')
                                .all())

                requests = dict_from_query(query)
                for request in requests:
                    query = (
                        session.query(db.attendee_table)
                                .filter_by(attendee_id=request['attendee_id'])
                                .one())

                    request['attendee_name'] = (
                        dict_from_query(query)['attendee_name'])

                # logging.info(query)

            self.render('admin.html', path='/admin', requests=requests)
        else:
            self.redirect('/')
            return


class LogoutHandler(BaseHandler):
    def get(self):
        self.set_secure_cookie('is_admin', json.dumps(False))
        self.redirect('/')
