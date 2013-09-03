import yaml


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
        files += [''] + parse_subsection(subsection[sub])

    return [
        (
            prefix + thing + postfix if thing != ''
            else ''
        )
        for thing in files
    ] if files else []


with open('includes.yaml') as fh:
    data = yaml.load(fh)

JS_INCLUDES = parse_subsection(data)
