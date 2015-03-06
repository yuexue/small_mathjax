'''
A simple tool for reducing the size of MathJax.
Base on https://github.com/mathjax/MathJax-docs/wiki/Guide%3A-reducing-size-of-a-mathjax-installation
'''
import sys
import os
import commands
import ConfigParser
import getopt

CONFIG = {
    'ROOT': 'MathJax',
    'keep': {
        'config': None,
        'localization': None,
        'extensions': None,
        'fonts': None,
        'font_formats': None,
        'input': None,
        'output': None
    },
    'dryrun': True,
    'total': 0
}


def get_size(path):
    status, output = commands.getstatusoutput("du %s -b --max-depth=0" % path)
    return int(output.split()[0])


def readable(size):
    size = float(size) / 1024.0
    if size < 1024:
        return '%3.3fK' % size
    else:
        size = size / 1024.0
        return '%3.3fM' % size


def remove(filepath):
    fullpath = "%s/%s" % (CONFIG['ROOT'], filepath)
    if os.path.exists(fullpath):
        if os.path.isfile(fullpath):
            size = get_size(fullpath)
            CONFIG['total'] += size
            print "Removing file %s(%s) ..." % (fullpath, readable(size))
        elif os.path.isdir(fullpath):
            size = get_size(fullpath)
            CONFIG['total'] += size
            print "Removing dir %s(%s) ..." % (fullpath, readable(size))
    if not CONFIG['dryrun']:
        os.system("rm -rf %s" % fullpath)


def remove_from(dirpath, keeped):
    dir_fullpath = '%s/%s' % (CONFIG['ROOT'], dirpath)
    for i in os.listdir(dir_fullpath):
        if i in keeped:
            continue
        remove('%s/%s' % (dirpath, i))


def remove_unnecessary():
    remove("docs")
    remove("test")
    remove("unpacked")
    remove(".gitignore")
    remove("README.md")
    remove("CONTRIBUTING.md")
    remove("bower.json")
    remove("composer.json")
    remove("LICENSE")


def remove_config(keeped=None):
    if keeped is None:
        keeped = []
    remove_from("config", keeped)


def remove_font_formats(keeped=None):
    if keeped is None:
        print("Warning: No font format is keeped.")
        keeped = []
    fonts_dir = "%s/%s" % (CONFIG['ROOT'], 'fonts/HTML-CSS')
    for font in os.listdir(fonts_dir):
        formats_dir = '%s/%s' % ('fonts/HTML-CSS', font)
        remove_from(formats_dir, keeped)


def remove_fonts(keeped=None):
    if keeped is None:
        print("Warning: No fonts is keeped.")
        keeped = []
    remove_from('fonts/HTML-CSS', keeped)
    remove_from('jax/output/SVG/fonts', keeped)
    remove_from('jax/output/HTML-CSS/fonts', keeped)


def remove_input(keeped=None):
    if keeped is None:
        print("Warning: No input is keeped.")
        keeped = []
    remove_from('jax/input', keeped)


def remove_output(keeped=None):
    if keeped is None:
        print("Warning: No output is keeped.")
        keeped = []
    remove_from('jax/output', keeped)


def remove_localization(keeped=None):
    if keeped is None:
        keeped = []
    remove_from("localization", keeped)


def remove_extensions(keeped=None):
    if keeped is None:
        keeped = []
    if 'HTML-CSS' not in keeped:
        remove('extensions/HTML-CSS/')
    if 'MathML' not in keeped:
        remove('extensions/MathML/')
    if 'TeX' not in keeped:
        remove('extensions/TeX/')


def run():
    remove_unnecessary()
    remove_config(keeped=CONFIG['keep']['config'])
    remove_localization(keeped=CONFIG['keep']['localization'])
    remove_extensions(keeped=CONFIG['keep']['extensions'])
    remove_input(keeped=CONFIG['keep']['input'])
    remove_output(keeped=CONFIG['keep']['output'])
    remove_fonts(keeped=CONFIG['keep']['fonts'])
    remove_font_formats(keeped=CONFIG['keep']['font_formats'])
    print("Size totally reduced %s." %
          (readable(CONFIG['total'])))
    print("The size of %s is %s." %
          (CONFIG['ROOT'], readable(get_size(CONFIG['ROOT']))))


def read_config(config_file):
    config = ConfigParser.ConfigParser()
    config.read(config_file)
    CONFIG['keep'] = {}
    for key, value in config.items('keep'):
        CONFIG['keep'][key] = value.strip().split()


def main():
    opts, args = getopt.gnu_getopt(sys.argv[1:], 'c:e', [])
    CONFIG['ROOT'] = args[0]
    if CONFIG['ROOT'].endswith('/'):
        CONFIG['ROOT'] = CONFIG['ROOT'][:-1]
    config_file = dict(opts)['-c']
    if '-e' in dict(opts):
        CONFIG['dryrun'] = False
    read_config(config_file)
    run()


if __name__ == '__main__':
    main()
