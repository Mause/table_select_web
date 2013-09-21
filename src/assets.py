#!/usr/bin/env python
import os
import re
import sys
import logging
import subprocess
from itertools import chain

import yaml
from settings import settings
from webassets import Environment, Bundle
from webassets.exceptions import FilterError
from webassets.filter import Filter, handlebars, register_filter


DIRNAME = os.path.abspath(os.path.dirname(__file__))
STATIC_DIR = os.path.abspath(os.path.join(DIRNAME, 'static/'))
GLOBAL_FILTERS = None

my_env = Environment(STATIC_DIR, '/static/')
my_env.debug = settings['release'].upper() == 'DEBUG'


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
            raise FilterError(
                ('ember-precompile: subprocess had error: stderr=%s, '
                 'stdout=%s, returncode=%s') % (stderr, stdout, proc.returncode))
        out_data = stdout.decode('utf-8').strip() + ';'
        out_data = out_data.replace('Ember.TEMPLATES["/', 'Ember.TEMPLATES["')
        out.write(out_data)

register_filter(EmberHandlebarsFilter)

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

    files += chain.from_iterable(
        parse_subsection(subsection[sub])
        for sub in order
    )

    return add_pre_post(prefix, postfix, files)


def sub_bundle(data, key, filters):
    js_files = parse_subsection(data['main'][key])
    js_files = add_pre_post('js/', '.js', js_files)

    js_bundle = Bundle(
        *js_files, filters=filters, output='gen/{}.js'.format(key))
    return js_bundle


def generate_js():
    with open(os.path.join(DIRNAME, 'js_assets.yaml')) as fh:
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
        my_env.register('combined',
                        *bundles,
                        filters=GLOBAL_FILTERS,
                        output='gen/combined.js')
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


def gen_assets():
    return '\n'.join(
        '<script src="{}"></script>'.format(filename)
        for filename in _gen_assets()
    )


def get_changed():
    modified = re.compile(r'^[MAD]  (?P<name>.*)')

    p = subprocess.Popen(['git', 'status', '--porcelain'], stdout=subprocess.PIPE)
    out, err = p.communicate()

    out = out.splitlines()
    out = (filename.decode('utf-8') for filename in out)
    actual_out = []
    for filename in out:
        match = modified.match(filename)
        if match:
            actual_out.append(match.groupdict()['name'])

    return actual_out


def has_changed(changed, filename):
    normalize = lambda x: '/'.join(re.split(r'[/\/]', x))

    filename = normalize(filename)

    for line in changed:
        line = normalize(line)

        if line.endswith(filename):
            return True

    return False


def main():
    GIT_HOOK = 'as_git_hook' in sys.argv
    should_regen = True

    if GIT_HOOK:
        print('Stashing uncommited code')
        return_code = subprocess.call(['git', 'stash', '--keep-index'], stdout=subprocess.PIPE)
        result = return_code or 0
        if result:
            sys.exit(result)

    try:
        if GIT_HOOK:
            changed = get_changed()

            changed = filter(
                lambda x: not x.endswith('combined.js'),
                changed
            )

            result = any(
                filename.rpartition('.')[-1] in ('hbs', 'js')
                for filename in changed
            )

            if not result:
                print('No assets have changed')
                should_regen = False

        if should_regen:
            my_env.debug = 'debug' in sys.argv

            ASSETS = _gen_assets()

            print('-----> Generated assets;')
            for asset in ASSETS:
                print('----->    ', asset)

                if 'as_git_hook' in sys.argv:
                    asset = asset.rpartition('?')[0]
                    cmd = ['git', 'add', DIRNAME + asset]

                    return_code = subprocess.call(cmd, stdout=subprocess.PIPE)
                    result = return_code or 0

                    if result:
                        # only break out of the loop, so we can reapply the stash
                        break

    finally:
        if GIT_HOOK:
            print('Restoring uncommited code')
            return_code = subprocess.call(['git', 'stash', 'pop'], stdout=subprocess.PIPE)
            result = return_code or 0
            if result:
                sys.exit(result)


if __name__ == '__main__':
    main()
