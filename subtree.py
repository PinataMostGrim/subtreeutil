'''

- Should be run from the repository's root folder
- Source must be a directory and cannot be a file
'''

import os
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
                               stderr=subprocess.PIPE,
                               shell=True)

    o, e = process.communicate()

    if o:
        print(o.decode('ascii'))
    if e:
        print(e.decode('ascii'))

    return o, e


def list_remotes():
    command = ['git', 'remote', '-v']
    o, e = execute_command(command)


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


def list_files():
    for dirpath, dirname, filenames in os.walk(CHECKOUT_SOURCE):
        for filename in filenames:
            full_path = Path(dirpath) / filename
            new_path = Path(CHECKOUT_DESTINATION) / full_path
            print('{} -> {}'.format(full_path, new_path))


# def move_files():
#     source = Path(CHECKOUT_SOURCE)
#     destination = Path(CHECKOUT_DESTINATION)

#     if not destination.exists():
#         destination.parent.mkdir(parents=True, exist_ok=True)

#     source.replace(destination)


def move_files():
    source = Path(CHECKOUT_SOURCE)

    for file in source.rglob('*'):
        source_file = Path(file)

        if source_file.is_dir():
            continue

        destination_file = Path(CHECKOUT_DESTINATION) / source_file.relative_to(CHECKOUT_SOURCE)

        print(f'Moving {source_file} -> {destination_file}')

        if not destination_file.parent.exists():
            destination_file.parent.mkdir(parents=True)

        source_file.replace(destination_file)


def cleanup():
    print(f'Cleaning up {CLEANUP}')
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
    # list_files()
    # list_remotes()


if __name__ == '__main__':
    main()
