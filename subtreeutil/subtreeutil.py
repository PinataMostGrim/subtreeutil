'''
Utility script for automating the checking out of folders from a remote repository.
'''

import subprocess

from pathlib import Path
from shutil import rmtree

from . import config


def perform_checkout(config_path: Path):
    config.load_config_file(config_path)

    remote_name = config.get_remote_name()
    remote_url = config.get_remote_url()
    branch = config.get_branch()
    source_paths = config.get_source_paths()
    destination_paths = config.get_destination_paths()
    cleanup_paths = config.get_cleanup_paths()

    print('')

    add_remote(remote_name, remote_url)
    fetch_remote(remote_name)

    commit_hash = get_remote_head_hash(remote_name, branch)
    # TODO: Log instead of print
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
        # TODO: Separate function and output using logging
        print(f'Moving contents of \'{source_path}\' -> \'{destination_path}\'')
        _move_folder(source_path, destination_path)

    if source_path.is_file():
        # TODO: Separate function and output using logging
        print(f'Moving \'{source_path}\' -> \'{destination_path}\'')
        _move_file(source_path, destination_path)


def _move_folder(source_folder: Path, destination_folder: Path):
    for file in source_folder.rglob('*'):
        source_file = Path(file)

        # Note: Skip moving folders as attempting to replace them seems to result in a
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
