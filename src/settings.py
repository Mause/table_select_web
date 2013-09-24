import os
import json
with open(os.path.join(os.path.dirname(__file__), 'settings.json')) as fh:
    settings = json.load(fh)

settings['DATABASE_URL'] = (os.environ.get("DATABASE_URL",
                                           settings.get('DATABASE_URL')))

flags = {
    'is_production': lambda: 'HEROKU' in os.environ,
    'is_staging': lambda: 'STAGING' in os.environ,
    'is_debug': lambda: not flags.is_production()
}

flags = type('flags', (object,), flags)
