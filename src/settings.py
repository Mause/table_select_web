import json
with open('settings.json') as fh:
    settings = json.load(fh)

import os
if 'HEROKU' in os.environ:
    settings['release'] = 'PRODUCTION'
