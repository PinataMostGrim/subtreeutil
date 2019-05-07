'''
Utility script for automating the checking out of folders from a remote repository.
'''

import json
import os
import subprocess

from pathlib import Path
from shutil import rmtree


_DEFAULT_CONFIG = {
    'remote_name': 'subtree',
    'remote_url': '',
    'branch': 'develop',
    'source_folder': '',
    'destination_folder': '',
    'cleanup_folder': ''
}


def perform_checkout(config):
    remote_name = config['remote_name']
    remote_url = config['remote_url']
    branch = config['branch']
    source_folder = config['source_folder']
    destination_folder = config['destination_folder']
    cleanup_folder = config['cleanup_folder']

    add_remote(remote_name, remote_url)
    fetch_remote(remote_name)

    checkout_remote_folder(
        remote_name,
        branch,
        source_folder)

    unstage_all()
    remove_remote(remote_name)

    if destination_folder:
        move_folder(
            Path(source_folder),
            Path(destination_folder))

    if cleanup_folder:
        cleanup_path = Path(cleanup_folder)
        if cleanup_path.exists() and cleanup_path.is_dir():
            delete_folder(cleanup_path)


def execute_command(command, log=True):
    print(' '.join(command))

    process = subprocess.Popen(command,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)

    o, e = process.communicate()

    if log:
        if o:
            print(o.decode('ascii'))
        if e:
            print(e.decode('ascii'))

    return o.decode('ascii'), e.decode('ascii')


def add_remote(remote_name, remote_url):
    command = ['git',
               'remote',
               'add',
               remote_name,
               remote_url]
    o, e = execute_command(command)


def remove_remote(remote_name):
    command = ['git', 'remote', 'remove', remote_name]
    o, e = execute_command(command)


def fetch_remote(remote_name):
    command = ['git', 'fetch', remote_name]
    o, e = execute_command(command)


def checkout_remote_folder(remote_name, remote_branch, folder_path: Path):
    command = ['git',
               'checkout',
               f'{_SUBTREE_NAME}/{subtree_branch}',
               folder_path]
    o, e = execute_command(command)


def unstage_all():
    command = ['git', 'reset']
    o, e = execute_command(command)


def move_folder(source_folder: Path, destination_folder: Path):
    print(f'Moving contents of \'{source_folder}\' -> \'{destination_folder}\'')

    for file in source_folder.rglob('*'):
        source_file = Path(file)

        # Skip folders as attempting to replace them seems to result in a
        # permission denied error.
        if source_file.is_dir():
            continue

        destination_file = destination_folder / source_file.relative_to(source_folder)

        if not destination_file.parent.exists():
            destination_file.parent.mkdir(parents=True)

        # print(f'Moving \'{source_file}\' -> \'{destination_file}\'')
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
