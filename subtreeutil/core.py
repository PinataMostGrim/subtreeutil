"""Automates checking out files and folders from a remote repository.
"""

import logging

from pathlib import Path
from shutil import rmtree

from . import config
from . command import execute_command


core_log = logging.getLogger('subtreeutil.core')


def perform_checkout(config_path: Path):
    """Performs the entire checkout operation using a configuration file.

    A full checkout operation includes the following steps:
    - Adds a remote repository
    - Fetches the remote
    - Checks out a list of sources (files or folders) from the remote
    - If destination paths are defined, will move sources to the matching destinations
    - Performs any configured cleanup (deletion of files or folders)
    - Removes the remote

    Args:
      config_path: Path: A Path object for the configuration file to perform the checkout operation with.
    """

    config.load_config_file(config_path)

    remote_name = config.get_remote_name()
    branch = config.get_branch()
    source_paths = config.get_source_paths()

    add_remote(remote_name, config.get_remote_url())
    fetch_remote(remote_name)

    commit_hash = get_remote_head_hash(remote_name, branch)
    core_log.info(f'Checking out files from {remote_name}/{branch} ({commit_hash})\n')

    for source_path in source_paths:
        checkout_remote_source(remote_name, branch, source_path)

    unstage_all()
    remove_remote(remote_name)

    # Note: zip() will stop as soon as the shortest list is exhausted.
    for source_path, destination_path in zip(
            source_paths,
            config.get_destination_paths()):
        move_source(Path(source_path), Path(destination_path))

    for cleanup_path in config.get_cleanup_paths():
        cleanup_path = Path(cleanup_path)
        delete_source(cleanup_path)

    core_log.info('Checkout complete!')


def add_remote(remote_name, remote_url):
    """Executes a 'git add remote' command.

    Args:
      remote_name: The remote repository's name.
      remote_url: The remote repository's URL.
    """

    command = ['git',
               'remote',
               'add',
               remote_name,
               remote_url]
    execute_command(command)


def remove_remote(remote_name):
    """Executes a 'git remove remote' command.

    Args:
      remote_name: The name of the remote to remove.
    """

    command = ['git', 'remote', 'remove', remote_name]
    execute_command(command)


def fetch_remote(remote_name):
    """Executes a 'git fetch' command on a remote.

    Args:
      remote_name: The name of the remote to fetch.
    """

    command = ['git', 'fetch', remote_name]
    execute_command(command)


def get_remote_head_hash(remote_name, branch):
    """Executes a 'git log' command to retrieve a branch's HEAD commit hash.

    Args:
      remote_name: The remote name to log.
      branch: The branch name to log.

    Returns:
        A string containing the commit hash with the format 'remote_name/branch_name (commit_hash)'
    """

    command = [
        'git', 'log', '-n', '1', f'{remote_name}/{branch}', '--pretty=format:%H']
    o, e = execute_command(command, display=False)
    return o


def checkout_remote_source(remote_name, remote_branch, source_path: Path):
    """Executes a 'git checkout' command to retrieve the source path from a remote.

    Args:
      remote_name:
      remote_branch:
      source_path: Path:
    """

    command = ['git',
               'checkout',
               f'{remote_name}/{remote_branch}',
               source_path]
    execute_command(command)


def unstage_all():
    """Executes a 'git reset' command."""

    command = ['git', 'reset']
    execute_command(command)


def move_source(source_path: Path, destination_path: Path):
    """Moves a source file or folder to a destination.

    Args:
      source_path: Path: A Path object for the source to move.
      destination_path: Path: A Path object for the destination to move the source to.
    """

    # TODO: Test exception handling in _move_folder() and _move_file()
    # Note: It would be better to allow an exception to occur rather than use a guard here. The problem is that an exception won't be caught by the _move_folder() method.
    if not source_path.exists():
        core_log.warning(f'{source_path} does not exist')
        return

    if source_path.is_dir():
        core_log.info(f'Moving contents of \'{source_path}\' -> \'{destination_path}\'')
        _move_folder(source_path, destination_path)

    if source_path.is_file():
        core_log.info(f'Moving \'{source_path}\' -> \'{destination_path}\'')
        _move_file(source_path, destination_path)


def _move_folder(source_folder: Path, destination_folder: Path):
    """Moves a folder and its contents to a new location.

    Args:
      source_folder: Path: A Path object for the source folder to move.
      destination_folder: Path: A Path object for the source folder's destination.
    """

    # TODO: Test for an exception if the folder doesn't exist
    for file in source_folder.rglob('*'):
        source_file = Path(file)

        # Note: Skip moving folders as attempting to replace them seems to result in a
        # permission denied error.
        if source_file.is_dir():
            continue

        destination_file = destination_folder / source_file.relative_to(source_folder)
        _move_file(source_file, destination_file)


def _move_file(source_file: Path, destination_file: Path):
    """Moves a file to a new location.

    Args:
      source_file: Path: A Path object for the source file to move.
      destination_file: Path: A Path object for the source file's destination.
    """

    # TODO: Use a try / except here
    if not destination_file.parent.exists():
        destination_file.parent.mkdir(parents=True)

    source_file.replace(destination_file)


def delete_source(cleanup_path: Path):
    """Deletes a file or folder.

    Args:
      cleanup_path: Path: A Path object for the file or folder to delete.
    """

    core_log.info(f'Deleting \'{cleanup_path}\'')

    if not cleanup_path.exists():
        core_log.warning(f'{cleanup_path} does not exist')
        return

    if cleanup_path.is_dir():
        _delete_folder(cleanup_path)

    if cleanup_path.is_file():
        _delete_file(cleanup_path)


def _delete_folder(folder_path: Path):
    """Deletes a folder and all of its contents.

    Args:
      folder_path: Path: A Path object for the folder to delete.
    """

    # TODO: Add try except here
    rmtree(folder_path)


def _delete_file(file_path: Path):
    """Deletes a file.

    Args:
      file_path: Path: A Path object for the file to delete.
    """

    # TODO: Add try except here
    file_path.unlink()
