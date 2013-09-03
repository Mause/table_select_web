

def add_all(pre, post, lst):
    return [pre + thing + post for thing in lst]


THIRD_PARTY_JS = add_all('js/third-party/', '.js', [
    'jquery',
    'handlebars',
    'ember',
    'ember-data',
    'bootstrap',
    'ember_plugins/ember-bootstrap'
])

CONTROLLERS = add_all('controllers/', '_controller.js', [
    'add_attendee',
    'admin',
    'attendee_list',
    'ball_table'
])

VIEWS = add_all('views/', '_view.js', [
    'add_attendee',
    'admin',
    'attendee_list',
    'ball_table',
    'removal_request_checkbox'
])

MIXINS = add_all('mixins/', '_mixin.js', [
    'error_handler'
])

MODELS = add_all('models/', '_model.js', [
    'attendee',
    'ball_table',
    'removal_request'
])

SUPPORT_OBJECTS = add_all('models/', '.js', [
    'adapter',
    'serializer',
    'store'
])

ROUTES = add_all('routes/', '_route.js', [
    'admin',
    'index',
    'info'
]) + add_all('routes/', '.js', [
    'router'
])

APP_JS = [
    'main.js',
    'handlebars_utils.js',
    'utils.js'
]

APP_JS += CONTROLLERS + VIEWS + MIXINS + ROUTES + MODELS + SUPPORT_OBJECTS
APP_JS = add_all('js/app/', '', APP_JS)


JS_INCLUDES = THIRD_PARTY_JS + APP_JS
