import os
import json
with open(os.path.join(os.path.dirname(__file__), 'settings.json')) as fh:
    settings = json.load(fh)

settings['DATABASE_URL'] = (
    os.environ.get("DATABASE_URL", settings.get('DATABASE_URL')))


if 'HEROKU' in os.environ:
    settings['release'] = 'PRODUCTION'


class Flags:
    def __init__(self):
        self.is_production = lambda: settings['release'].upper() == "PRODUCTION"

flags = Flags()
