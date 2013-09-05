import os
import subprocess

import yaml
from settings import settings
from webassets import Environment, Bundle
from webassets.exceptions import FilterError
from webassets.filter import Filter, handlebars, register_filter

add_pre_post = lambda pre, post, lst: [pre + thing + post for thing in lst]


class EmberHandlebarsFilter(handlebars.Handlebars, Filter):
    name = 'ember_handlebars'

    def process_templates(self, out,  hunks, **kw):
        templates = [info['source_path'] for _, info in hunks]

        if self.root is True:
            root = self.get_config('directory')
        elif self.root:
            root = os.path.join(self.get_config('directory'), self.root)
        else:
            root = self._find_base_path(templates)

        args = [self.binary or 'ember-precompile']
        if root:
            args.extend(['-b', root + '/'])
        if self.extra_args:
            args.extend(self.extra_args)
        args.extend(templates)

        proc = subprocess.Popen(
            args, stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate()

        if proc.returncode != 0:
            raise FilterError(
                ('ember-precompile: subprocess had error: stderr=%s, '
                 'stdout=%s, returncode=%s') % (stderr, stdout, proc.returncode))
        out_data = stdout.decode('utf-8').strip() + ';'
        out_data = out_data.replace('Ember.TEMPLATES["/', 'Ember.TEMPLATES["')
        out.write(out_data)

register_filter(EmberHandlebarsFilter)


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
    dirname = os.path.dirname(__file__)
    with open(os.path.join(dirname, 'includes.yaml')) as fh:
        data = yaml.load(fh)

    static_dir = os.path.join(dirname, 'static/')
    my_env = Environment(static_dir, '/static/')

    filters = None  # 'jsmin'

    # third party libraries
    third_party_bundle = sub_bundle(data, 'third_party', filters)
    my_env.register('js_third_party', third_party_bundle)

    # application specific
    app_bundle = sub_bundle(data, 'app', filters)
    my_env.register('js_app', app_bundle)

    # precompiled templates
    handlebars_template_bundle = Bundle(
        'templates/*.hbs',
        'templates/components/*.hbs',
        filters='ember_handlebars',
        output='js/compiled_templates.js'
    )
    my_env.register('handlebars_templates', handlebars_template_bundle)

    my_env.debug = settings['release'].upper() == 'DEBUG'

    JS_INCLUDES = (
        my_env['js_third_party'].urls() +
        my_env['js_app'].urls() +
        my_env['handlebars_templates'].urls()
    )

    return JS_INCLUDES


def js_includes():
    return '\n'.join(
        '<script src="{}"></script>'.format(filename)
        for filename in generate_includes()
    )
