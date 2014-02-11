import re
import time
import hmac
import base64
import logging

from settings import settings

AUTH_RE = re.compile(r'(\w+) (.*)')
SEP = str(base64.b64encode(b'DOM'))[2:-1]

API_KEY_SEED = settings['api_key_seed'].encode('utf-8') or b'bytes'


class AuthorizedEndpoint(object):
    def is_authenticated(self):
        if 'Authorization' not in self.headers:
            logging.info(
                'Attempted to access restricted endpoint '
                'without authentication'
            )
            return False
        else:
            auth_data = self.headers['Authorization']
            match = AUTH_RE.match(auth_data)
            if match:
                auth_type = match.groups()[0]
                if auth_type == 'none':
                    logging.info(
                        'Attempted to access restricted endpoint with '
                        '"none" authentication'
                    )
                    return False
                elif auth_type == 'Bearer':
                    key = match.groups()[1]

                    if self.verify_key(key):
                        return True
                    else:
                        logging.info(
                            'Attempted to access restricted endpoint with '
                            'invalid authentication key'
                        )
                else:
                    self.set_bad_error(401)
            else:
                logging.info(
                    'Attempted to access restricted endpoint '
                    'with invalid authentication'
                )

    def verify_key(self, key):
        user_hash, timestamp = key.split(SEP)

        timestamp = base64.b64decode(timestamp.encode('utf-8'))
        timestamp = float(timestamp.decode('utf-8'))

        possible_users = {
            hmac.new(API_KEY_SEED, username.encode('utf-8')).hexdigest()
            for username in settings['auth_combos'].keys()
        }

        if timestamp > time.time():
            logging.info('Invalid key, timestamp in future')
            return False

        elif user_hash not in possible_users:
            logging.info('No such user hash')
            return False

        else:
            return True

    def create_key(self, username):
        user_hash = hmac.new(API_KEY_SEED, username).hexdigest()

        timestamp = str(time.time())
        timestamp = timestamp.encode('utf-8')
        timestamp = str(base64.b64encode(timestamp))[2:-1]

        ret = '{}{}{}'.format(
            user_hash,
            SEP,
            timestamp
        )
        if "b'" in ret:
            import code
            code.interact(local=locals())
        return ret
