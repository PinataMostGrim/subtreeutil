'''

- Best to be run from the repository's root folder
- Source must be a directory and cannot be a file
'''

import subprocess

from pathlib import Path
from shutil import rmtree


FRAMEWORK_NAME = ''
FRAMEWORK_URL = ''

CHECKOUT_SOURCE = ''
CHECKOUT_DESTINATION = 
CLEANUP = ''


def execute_command(command):
    print(' '.join(command))

    process = subprocess.Popen(command,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)

    o, e = process.communicate()

    if o:
        print(o.decode('ascii'))
    if e:
        print(e.decode('ascii'))

    return o, e


def add_framework():
    command = ['git',
               'remote',
               'add',
               FRAMEWORK_NAME,
               FRAMEWORK_URL]
    o, e = execute_command(command)


def remove_framework():
    command = ['git', 'remote', 'remove', FRAMEWORK_NAME]
    o, e = execute_command(command)


def fetch_framework():
    command = ['git', 'fetch', FRAMEWORK_NAME]
    o, e = execute_command(command)


def checkout_framework():
    command = ['git',
               'checkout',
               '{}/develop'.format(FRAMEWORK_NAME),
               CHECKOUT_SOURCE]
    o, e = execute_command(command)


def unstage_all():
    command = ['git', 'reset']
    o, e = execute_command(command)


def move_files():
    source = Path(CHECKOUT_SOURCE)

    for file in source.rglob('*'):
        source_file = Path(file)

        # Skip folders as attempting to replace them seems to result in a
        # permission denied error.
        if source_file.is_dir():
            continue

        destination_file = Path(CHECKOUT_DESTINATION) / source_file.relative_to(CHECKOUT_SOURCE)

        print(f'Moving \'{source_file}\' -> \'{destination_file}\'')

        if not destination_file.parent.exists():
            destination_file.parent.mkdir(parents=True)

        source_file.replace(destination_file)


def cleanup():
    print(f'Cleaning up \'{CLEANUP}\'')

    source = Path(CLEANUP)
    rmtree(source)


def main():
    add_framework()
    fetch_framework()
    checkout_framework()
    unstage_all()
    remove_framework()
    move_files()
    cleanup()


if __name__ == '__main__':
    main()
