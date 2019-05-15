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
    'source_paths': [],
    'destination_paths': [],
    'cleanup_paths': []
}


def perform_checkout(config):
    remote_name = config['remote_name']
    remote_url = config['remote_url']
    branch = config['branch']
    source_paths = config['source_paths']
    destination_paths = config['destination_paths']
    cleanup_paths = config['cleanup_paths']

    print('')

    add_remote(remote_name, remote_url)
    fetch_remote(remote_name)

    commit_hash = get_remote_head_hash(remote_name, branch)
    print(f'\nChecking out files from {remote_name}/{branch} ({commit_hash})\n')

    for source_path in source_paths:
        checkout_remote_folder(
            remote_name,
            branch,
            source_path)

    unstage_all()
    remove_remote(remote_name)

    # Note: zip will stop as soon as the shortest list is exhausted.
    for source_path, destination_path in zip(source_paths, destination_paths):
        move_source(
            Path(source_path),
            Path(destination_path))

    for cleanup_path in cleanup_paths:
        cleanup_path = Path(cleanup_path)
        delete_source(cleanup_path)


def execute_command(command, log=True):
    if log:
        print(' '.join(command))

    process = subprocess.Popen(command,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)

    o, e = process.communicate()

    # TODO: Separate function and output using logging
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


def get_remote_head_hash(remote_name, branch):
    command = [
        'git', 'log', '-n', '1', f'{remote_name}/{branch}', '--pretty=format:%H']
    o, e = execute_command(command, log=False)
    return o


def checkout_remote_folder(remote_name, remote_branch, folder_path: Path):
    command = ['git',
               'checkout',
               f'{remote_name}/{remote_branch}',
               folder_path]
    o, e = execute_command(command)


def unstage_all():
    command = ['git', 'reset']
    o, e = execute_command(command)


def move_source(source_path: Path, destination_path: Path):
    if not source_path.exists():
        # TODO: Separate function and output using logging
        print(f'{source_path} does not exist')
        return

    if source_path.is_dir():
        print(f'Moving contents of \'{source_path}\' -> \'{destination_path}\'')
        _move_folder(source_path, destination_path)

    if source_path.is_file():
        print(f'Moving \'{source_path}\' -> \'{destination_path}\'')
        _move_file(source_path, destination_path)


def _move_folder(source_folder: Path, destination_folder: Path):
    for file in source_folder.rglob('*'):
        source_file = Path(file)

        # Skip moving folders as attempting to replace them seems to result in a
        # permission denied error.
        if source_file.is_dir():
            continue

        destination_file = destination_folder / source_file.relative_to(source_folder)
        _move_file(source_file, destination_file)


def _move_file(source_file: Path, destination_file: Path):
    if not destination_file.parent.exists():
        destination_file.parent.mkdir(parents=True)

    source_file.replace(destination_file)


def delete_source(cleanup_path: Path):
    if not cleanup_path.exists():
        print(f'{cleanup_path} does not exist')
        return

    print(f'Deleting \'{cleanup_path}\'')

    if cleanup_path.is_dir():
        _delete_folder(cleanup_path)

    if cleanup_path.is_file():
        _delete_file(cleanup_path)


def _delete_folder(folder_path: Path):
    # TODO: Try except here?
    rmtree(folder_path)


def _delete_file(file_path: Path):
    # TODO: Try except here?
    file_path.unlink()


def load_config(config: Path):
    # TODO: Try except here?
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
        json.dump(_DEFAULT_CONFIG, f, indent=4)
