"""Automates checking out files and folders from a remote repository."""

import logging

from pathlib import Path

from . import config
from . import command as commandutil


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
      config_path: Path: A Path object for the configuration file to perform the
      checkout operation with.
    """

    config.load_config_file(config_path)

    # TODO: Handle case where an existing repository doesn't exist

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
    for source_path, destination_path in zip(source_paths, config.get_destination_paths()):
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

    command = ['git', 'remote', 'add', remote_name, remote_url]
    commandutil.execute_command(command)


def remove_remote(remote_name):
    """Executes a 'git remove remote' command.

    Args:
      remote_name: The name of the remote to remove.
    """

    command = ['git', 'remote', 'remove', remote_name]
    commandutil.execute_command(command)


def fetch_remote(remote_name):
    """Executes a 'git fetch' command on a remote.

    Args:
      remote_name: The name of the remote to fetch.
    """

    command = ['git', 'fetch', remote_name]
    commandutil.execute_command(command)


def get_remote_head_hash(remote_name, branch):
    """Executes a 'git log' command to retrieve a branch's HEAD commit hash.

    Args:
      remote_name: The remote name to log.
      branch: The branch name to log.

    Returns:
        A string containing the commit hash with the format 'remote_name/branch_name (commit_hash)'
    """

    command = ['git', 'log', '-n', '1', f'{remote_name}/{branch}', '--pretty=format:%H']
    o, e = commandutil.execute_command(command, display=False)
    return o


def checkout_remote_source(remote_name, remote_branch, source_path: Path):
    """Executes a 'git checkout' command to retrieve the source path from a remote.

    Args:
      remote_name: The remote name to check out from.
      remote_branch: The remote branch to check out from.
      source_path: Path: A Path object for the file or folder to checkout from the remote branch.
    """

    command = ['git', 'checkout', f'{remote_name}/{remote_branch}', source_path]
    commandutil.execute_command(command)


def unstage_all():
    """Executes a 'git reset' command."""

    command = ['git', 'reset']
    commandutil.execute_command(command)


def move_source(source_path: Path, destination_path: Path):
    """Moves a source file or folder to a destination.

    Args:
      source_path: Path: A Path object for the source to move.
      destination_path: Path: A Path object for the destination to move the source to.
    """

    try:
        if source_path.is_dir():
            core_log.info(f'Moving contents of \'{source_path}\' -> \'{destination_path}\'')
            commandutil.move_folder(source_path, destination_path)

        if source_path.is_file():
            core_log.info(f'Moving \'{source_path}\' -> \'{destination_path}\'')
            commandutil.move_file(source_path, destination_path)
    except (commandutil.MoveCommandError, commandutil.DeleteCommandError):
        # Exceptions of these types are already logged in lower level functions.
        # We simply want to intercept and continue as an error moving isn't the end of the world.
        pass


def delete_source(cleanup_path: Path):
    """Deletes a file or folder.

    Args:
      cleanup_path: Path: A Path object for the file or folder to delete.
    """

    core_log.info(f'Deleting \'{cleanup_path}\'')

    # TODO: Test whether we need this guard if the command.delete methods handle exception catching
    if not cleanup_path.exists():
        core_log.warning(f'{cleanup_path} does not exist')
        return

    try:
        if cleanup_path.is_dir():
            commandutil.delete_folder(cleanup_path)

        if cleanup_path.is_file():
            commandutil.delete_file(cleanup_path)
    except commandutil.DeleteCommandError:
        # Note: OSErrors here are not necessarily fatal and application execution
        # should continue.
        pass
