import yaml
from settings import settings
from webassets import Environment, Bundle

add_pre_post = lambda pre, post, lst: [pre + thing + post for thing in lst]


def parse_subsection(subsection):
    if not subsection:
        return []

    if 'prefix' in subsection and subsection['prefix']:
        prefix = subsection['prefix']
        del subsection['prefix']
    else:
        prefix = ''

    if 'postfix' in subsection and subsection['postfix']:
        postfix = subsection['postfix']
        del subsection['postfix']
    else:
        postfix = ''

    if 'files' in subsection and subsection['files']:
        files = subsection['files']
        del subsection['files']
    else:
        files = []

    order = subsection['order'] if 'order' in subsection else subsection

    for sub in order:
        files += parse_subsection(subsection[sub])

    return add_pre_post(prefix, postfix, files)


def sub_bundle(data, key, filters):
    js_files = parse_subsection(data['main'][key])
    js_files = add_pre_post('js/', '.js', js_files)

    js_bundle = Bundle(
        *js_files, filters=filters, output='js/{}.js'.format(key))
    return js_bundle


def generate_includes():
    with open('includes.yaml') as fh:
        data = yaml.load(fh)

    my_env = Environment('static/', 'static/')
    my_env.config['HANDLEBARS_BIN'] = 'ember-precompile'

    filters = None  # 'jsmin'

    # third party libraries
    third_party_bundle = sub_bundle(data, 'third_party', filters)
    my_env.register('js_third_party', third_party_bundle)

    # application specific
    app_bundle = sub_bundle(data, 'app', filters)
    my_env.register('js_app', app_bundle)

    # precompiled templates
    handlebars_template_bundle = Bundle(
        'templates/*.handlebars',
        filters='handlebars',
        output='js/compiled_templates.js'
    )
    my_env.register('handlebars_templates', handlebars_template_bundle)

    my_env.debug = settings['release'].upper() == 'DEBUG'

    JS_INCLUDES = (
        my_env['js_third_party'].urls() +
        my_env['js_app'].urls() +
        my_env['handlebars_templates'].urls()
    )

    return add_pre_post('/', '', JS_INCLUDES)


def js_includes():
    return '\n'.join([
        '<script src="{}"></script>'.format(filename)
        for filename in generate_includes()
    ])
