import os
import glob


def main():
    import sys
    if len(sys.argv) > 3:
        sys.exit('Too many args')
    elif len(sys.argv) == 1:
        out_file = '../../templates/templates.html'
        in_dir = '.'
    elif len(sys.arg) == 2:
        out_file = sys.argv[1]
        in_dir = '.'
    elif len(sys.argv) == 3:
        out_file = sys.argv[1]
        in_dir = sys.argv[2]

    compact(out_file, in_dir)


def compact(out_file, in_dir):
    in_dir = os.path.join(in_dir, '*.hbs')

    filenames = list(glob.glob(in_dir))

    start = '<script type="text/x-handlebars" data-template-name="{}">\n'
    end = '</script>\n\n'

    for filename in filenames:
        if filename.endswith('_navigation.hbs'):
            del filenames[filenames.index(filename)]
            filenames.append(filename)
            break

    with open(out_file, 'w') as out_fh:
        out_fh.write('{% extends "base.html" %}\n')
        out_fh.write('{% block content %}\n')

        for filename in filenames:
            with open(os.path.join(os.getcwd(), filename))as fh:
                content = fh.readlines()

            filename = filename.split('.')[-2].split(os.sep)[-1]

            out_fh.write('\t' * 2 + start.format(filename))
            for line in content:
                line = line.replace('{{', '{{!')
                out_fh.write('\t' * 2 + '\t{}'.format(line))
            out_fh.write('\t' * 2 + end)

        out_fh.write('{% end %}\n')

if __name__ == '__main__':
    main()
