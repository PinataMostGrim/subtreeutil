'''

'''

import subprocess

from pathlib import Path
from shutil import rmtree


SUBTREE_NAME = 'subtree'


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


def add_subtree(subtree_url):
    command = ['git',
               'remote',
               'add',
               SUBTREE_NAME,
               subtree_url]
    o, e = execute_command(command)


def remove_subtree():
    command = ['git', 'remote', 'remove', SUBTREE_NAME]
    o, e = execute_command(command)


def fetch_subtree():
    command = ['git', 'fetch', SUBTREE_NAME]
    o, e = execute_command(command)


def checkout_subtree_folder(subtree_branch, folder_path: Path):
    command = ['git',
               'checkout',
               f'{SUBTREE_NAME}/{subtree_branch}',
               folder_path]
    o, e = execute_command(command)


def unstage_all():
    command = ['git', 'reset']
    o, e = execute_command(command)


def move_folder(source_folder: Path, destination_folder: Path):
    for file in source_folder.rglob('*'):
        source_file = Path(file)

        # Skip folders as attempting to replace them seems to result in a
        # permission denied error.
        if source_file.is_dir():
            continue

        destination_file = destination_folder / source_file.relative_to(source_folder)

        print(f'Moving \'{source_file}\' -> \'{destination_file}\'')

        if not destination_file.parent.exists():
            destination_file.parent.mkdir(parents=True)

        source_file.replace(destination_file)


def delete_folder(folder: Path):
    if not folder.is_dir():
        print(f'{folder} is not a folder')
        return

    print(f'Deleting \'{folder}\'')

    rmtree(folder)
