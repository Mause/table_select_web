import os
import json
with open(os.path.join(os.path.dirname(__file__), 'settings.json')) as fh:
    settings = json.load(fh)

if 'HEROKU' in os.environ:
    settings['release'] = 'PRODUCTION'
