'''

'''

import json
import os
import subprocess

from pathlib import Path
from shutil import rmtree


_SUBTREE_NAME = 'subtree'
_DEFAULT_CONFIG = {
    'remote_url': '',
    'branch': 'develop',
    'source_folder': '',
    'destination_folder': '',
    'cleanup_folder': ''
}


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


def perform_checkout(config):
    remote_url = config['remote_url']
    branch = config['branch']
    source_folder = config['source_folder']
    destination_folder = config['destination_folder']
    cleanup_folder = config['cleanup_folder']

    add_subtree(remote_url)
    fetch_subtree()

    checkout_subtree_folder(
        branch,
        source_folder)

    unstage_all()
    remove_subtree()

    if destination_folder:
        move_folder(
            Path(source_folder),
            Path(destination_folder))

    if cleanup_folder:
        cleanup_path = Path(cleanup_folder)
        if cleanup_path.exists() and cleanup_path.is_dir():
            delete_folder(cleanup_path)


def add_subtree(subtree_url):
    command = ['git',
               'remote',
               'add',
               _SUBTREE_NAME,
               subtree_url]
    o, e = execute_command(command)


def remove_subtree():
    command = ['git', 'remote', 'remove', _SUBTREE_NAME]
    o, e = execute_command(command)


def fetch_subtree():
    command = ['git', 'fetch', _SUBTREE_NAME]
    o, e = execute_command(command)


def checkout_subtree_folder(subtree_branch, folder_path: Path):
    command = ['git',
               'checkout',
               f'{_SUBTREE_NAME}/{subtree_branch}',
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


def load_config(config: Path):
    with config.open('r') as f:
        data = json.load(f)

    return data


def edit_config(config: Path):
    if not config.suffix == '.json':
        config = config.with_suffix('.json')

    if not config.exists():
        create_default_config(config)

    try:
        # Windows
        os.startfile(str(config))
    except AttributeError:
        # OSX / Linux
        subprocess.Popen(['open', str(config)])


def create_default_config(config: Path):
    with config.open(mode='w') as f:
        json.dump(_DEFAULT_CONFIG, f, indent=2)
