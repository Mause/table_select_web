#!/usr/bin/env python
from os.path import abspath, dirname, join
import sys
import logging
import subprocess
from itertools import chain

import yaml
from settings import flags
from webassets import Environment, Bundle
from webassets.exceptions import FilterError
from webassets.filter import Filter, handlebars, register_filter


DIRNAME = abspath(dirname(__file__))
STATIC_DIR = abspath(join(DIRNAME, 'static/'))
GLOBAL_FILTERS = 'rjsmin'

my_env = Environment(STATIC_DIR, '/static/')
my_env.debug = flags.is_debug()


class EmberHandlebarsFilter(handlebars.Handlebars, Filter):
    name = 'ember_handlebars'

    def process_templates(self, out,  hunks, **kw):
        templates = [info['source_path'] for _, info in hunks]

        if self.root is True:
            root = self.get_config('directory')
        elif self.root:
            root = join(self.get_config('directory'), self.root)
        else:
            root = self._find_base_path(templates)

        args = [self.binary or 'ember-precompile']
        if root:
            args.extend(['-b', root + '/'])

        args.extend(['-k', 'each', '-k', 'if'])

        if self.extra_args:
            args.extend(self.extra_args)
        args.extend(templates)

        proc = subprocess.Popen(
            args, stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate()

        if proc.returncode != 0:
            msg = (
                'ember-precompile: subprocess had error: stderr=%s, '
                'stdout=%s, returncode=%s'
            ) % (stderr, stdout, proc.returncode)
            raise FilterError(msg)

        out_data = stdout.decode('utf-8').strip() + ';'
        out_data = out_data.replace('Ember.TEMPLATES["/', 'Ember.TEMPLATES["')
        out.write(out_data)

register_filter(EmberHandlebarsFilter)

add_pre_post = lambda pre, post, lst: [pre + thing + post for thing in lst]


def parse_subsection(subsection):
    if not subsection:
        return []

    prefix = subsection.pop('prefix') if subsection.get('prefix') else ''
    postfix = subsection.pop('postfix') if subsection.get('postfix') else ''
    files = subsection.pop('files') if subsection.get('files') else []
    order = subsection.pop('order') if subsection.get('order') else subsection

    extra_files = map(subsection.__get__, order)
    extra_files = map(parse_subsection, order)
    files += chain.from_iterable(extra_files)

    return add_pre_post(prefix, postfix, files)


def sub_bundle(data, key, filters):
    js_files = parse_subsection(data['main'][key])
    js_files = add_pre_post('js/', '.js', js_files)

    return Bundle(
        *js_files,
        filters=filters,
        output='gen/{}.js'.format(key)
    )


def generate_js():
    with open(join(DIRNAME, 'js_assets.yaml')) as fh:
        data = yaml.load(fh)

    # third party libraries
    if 'js_third_party' not in my_env:
        third_party_bundle = sub_bundle(data, 'third_party', GLOBAL_FILTERS)
        my_env.register('js_third_party', third_party_bundle)

    # application specific
    if 'js_app' not in my_env:
        app_bundle = sub_bundle(data, 'app', GLOBAL_FILTERS)
        my_env.register('js_app', app_bundle)


def generate_templates():
    # precompiled templates
    if 'handlebars_templates' not in my_env:
        handlebars_template_bundle = Bundle(
            'templates/*.hbs',
            'templates/components/*.hbs',
            filters='ember_handlebars',
            output='gen/compiled_templates.js'
        )
        my_env.register('handlebars_templates', handlebars_template_bundle)


def combine_bundles(*bundles):
    if 'combined' not in my_env:
        my_env.register(
            'combined',
            *bundles,
            filters=GLOBAL_FILTERS,
            output='gen/combined.js'
        )
    return my_env['combined'].urls()


def _gen_assets():
    generate_js()
    generate_templates()

    if my_env.debug:
        JS_INCLUDES = (
            my_env['js_third_party'].urls() +
            my_env['js_app'].urls() +
            my_env['handlebars_templates'].urls()
        )
    else:
        logging.debug('Combining bundles...')
        JS_INCLUDES = combine_bundles(
            my_env['js_third_party'],
            my_env['js_app'],
            my_env['handlebars_templates']
        )
    return JS_INCLUDES


def gen_assets_tags():
    return '\n'.join(
        '<script src="{}"></script>'.format(filename)
        for filename in _gen_assets()
    )


def main():
    my_env.debug = 'debug' in sys.argv
    ASSETS = _gen_assets()

    print('-----> Generated assets;')
    for asset in ASSETS:
        print('----->    ', asset)


if __name__ == '__main__':
    main()
