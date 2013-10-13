import os
import json
with open(os.path.join(os.path.dirname(__file__), 'settings.json')) as fh:
    settings = json.load(fh)

settings['DATABASE_URL'] = (os.environ.get("DATABASE_URL",
                                           settings['DATABASE_URL']))


class Flags(object):
    is_production = lambda self=None: 'HEROKU' in os.environ
    is_staging = lambda self=None: 'STAGING' in os.environ
    is_debug = lambda self=None: not flags.is_production()

flags = Flags()
