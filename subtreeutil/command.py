"""Executes commands using the subprocess module and handles OS level operations."""

import logging
import os
import subprocess

from pathlib import Path
from shutil import rmtree


command_log = logging.getLogger('subtreeutil.command')


class CommandError(Exception):
    """Base error for command module exceptions."""


class DeleteCommandError(CommandError):
    """An error occured while attempting to delete a file or folder."""


def execute_command(command: list, display=True):
    """Executes a command process using the subprocesses module.

    Used primarily for executing git commands.

    Args:
      command: list: The command to execute.
      display:  (Default value = True) Displays the command parameter in the console if True.

    Returns:
        A tuple containing stdout and stderr for the executed command.
    """

    if display:
        command_log.info(' '.join(command))
    else:
        command_log.debug(' '.join(command))

    with subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE) as process:
        o, e = process.communicate()

    if display and o:
        command_log.info(o.decode('ascii'))
    else:
        command_log.debug(o.decode('ascii'))

    if e:
        command_log.error(e.decode('ascii'))

    return o.decode('ascii'), e.decode('ascii')


def open_file(file_path: Path):
    """Opens a file using the default system application.

    Args:
      file_path: Path: The file to open.
    """

    command_log.info(f'Opening \'{file_path}\'')
    try:
        # Note: Open file in Windows
        os.startfile(str(file_path))
    except AttributeError:
        # Note: Open file in OSX / Linux
        command = ['open', str(file_path)]
        execute_command(command)


def delete_folder(folder_path: Path):
    """Deletes a folder and all of its contents.

    Args:
      folder_path: Path: A Path object for the folder to delete.

    Raises:
      DeleteCommandError: An OSError occured while attempting to delete a folder.
    """

    try:
        rmtree(folder_path)
    except OSError as exception:
        command_log.warning(f'Unable to delete \'{folder_path}\', {exception}')
        raise DeleteCommandError(f'Unable to delete \'{folder_path}\', {exception}')


def delete_file(file_path: Path):
    """Deletes a file.

    Args:
      file_path: Path: A Path object for the file to delete.

    Raises:
      DeleteCommandError: An OSError occured while attempting to delete a file.
    """

    try:
        file_path.unlink()
    except OSError as exception:
        command_log.warning(f'Unable to delete \'{file_path}\', {exception}')
        raise DeleteCommandError(f'Unable to delete \'{file_path}\', {exception}')
