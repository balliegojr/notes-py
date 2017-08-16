"""Note manager.

Usage:
  notes.py (insert | new) [--editor=<$editor>] <note>...
  notes.py (remove | del) <note>...
  notes.py edit [--editor=<$editor>] <note>...
  notes.py show <note>...
  notes.py (move | rename) <note> <dst>
  notes.py list
  notes.py

  notes.py (-h | --help)
  notes.py --version

Options:
  -h --help             Show this screen.
  --version             Show version.
  --editor $editor      force the use of an editor
"""

import os
import os.path
import configparser
import shlex
import shutil
from docopt import docopt

__version__ = '0.1'

config_path = os.path.expanduser('~/.notesrc')
base_path = ''
base_extension = None
editor = None


def new_note(note_path):
    path = os.path.normpath(os.path.join(base_path, note_path + base_extension))

    if os.path.exists(path):
        raise Exception('Note already exists')

    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))

    os.system('{0} {1}'.format(editor, shlex.quote(path)))

    clear_empty_dir(os.path.dirname(path))


def list_notes():
    print("Notes")
    os.system("tree -C -l --noreport -- {1} | tail -n +2 | sed -E 's/\{0}(\\x1B\\[[0-9]+m)?( ->|$)/\\1\\2/g'".format(base_extension, base_path))


def edit_note(note_path):
    path = os.path.join(base_path, note_path + base_extension)

    if not os.path.exists(path):
        raise Exception('Note do not exist')

    os.system('{0} {1}'.format(editor, shlex.quote(path)))


def show_note(note_path):
    path = os.path.join(base_path, note_path + base_extension)

    if not os.path.exists(path):
        raise Exception('Note do not exist')

    os.system('cat {0}'.format(shlex.quote(path)))


def remove_note(note_path):
    path = os.path.join(base_path, note_path + base_extension)

    if os.path.exists(path):
        os.remove(path)

    clear_empty_dir(os.path.dirname(path))


def rename_note(note_path, new_note_path):
    src = os.path.join(base_path, note_path + base_extension)
    dst = os.path.join(base_path, new_note_path + base_extension)

    if not os.path.exists(src):
        raise Exception('Note do not exist')

    if os.path.exists(dst):
        raise Exception('Note already exists')

    shutil.move(src, dst)
    clear_empty_dir(os.path.dirname(src))


def check_basepath():
    if not os.path.exists(base_path):
        os.makedirs(base_path)


def clear_empty_dir(path):
    if path == base_path:
        return

    if len(os.listdir(path)) == 0:
        os.removedirs(path)


def load_config():
    global base_path
    global base_extension
    global editor

    if not os.path.exists(config_path):
        config = configparser.ConfigParser()
        config['NOTES'] = {
            'path': '~/.notes',
            'extension': '.note',
            'editor': '$EDITOR'
        }

        with open(config_path, 'w') as configfile:
            config.write(configfile)

    else:
        config = configparser.ConfigParser()
        config.read(config_path)

    base_path = os.path.expanduser(config['NOTES']['path'])
    base_extension = config['NOTES']['extension']
    editor = config['NOTES']['editor']


def main(args):
    load_config()
    check_basepath()

    note = args['<note>']
    if isinstance(note, list):
        note = ' '.join(note)

    if args['--editor']:
        global editor
        editor = args['--editor']

    if args['list']:
        list_notes()
    elif args['new'] or args['insert']:
        new_note(note)
    elif args['edit']:
        edit_note(note)
    elif args['show']:
        show_note(note)
    elif args['del'] or args['remove']:
        remove_note(note)
    elif args['move'] or args['rename']:
        rename_note(note, args['<dst>'])
    else:
        list_notes()


if __name__ == "__main__":
    args = docopt(__doc__, version=__version__)

    try:
        main(args)
    except Exception as ex:
        print(ex)
