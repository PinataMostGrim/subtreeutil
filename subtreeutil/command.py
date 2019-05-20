"""Executes commands using the subprocess module and handles OS level operations."""

import logging
import os
import subprocess

from pathlib import Path
from shutil import rmtree


command_log = logging.getLogger('subtreeutil.command')


class CommandError(Exception):
    """Base error for command module exceptions."""


class MoveCommandError(CommandError):
    """An error occured while attempting to move a file or folder."""


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

    with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as process:
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


def move_folder(source_folder: Path, destination_folder: Path):
    """Moves a folder and its contents to a new location.

    Args:
      source_folder: Path: A Path object for the source folder to move.
      destination_folder: Path: A Path object for the source folder's destination.

    Raises:
      MoveCommandError: An OSError occurred while attempting to move the folder's
        contents, or the folder does not exist.
    """

    if source_folder == destination_folder:
        return

    if not source_folder.exists():
        command_log.warning(f'Unable to move \'{source_folder}\', folder does not exist')
        raise MoveCommandError(f'Unable to move \'{source_folder}\', folder does not exist')

    for file in source_folder.rglob('*'):
        source_file = Path(file)

        # Note: Skip moving folders as attempting to replace them seems to result in a
        # permission denied error.
        if source_file.is_dir():
            continue

        destination_file = destination_folder / source_file.relative_to(source_folder)
        move_file(source_file, destination_file)

    delete_folder(source_folder)


def move_file(source_file: Path, destination_file: Path):
    """Moves a file to a new location.

    Args:
      source_file: Path: A Path object for the source file to move.
      destination_file: Path: A Path object for the source file's destination.

    Raises:
      MoveCommandError: An OSError occurred while attempting to move a file, or the file
        does not exist.
    """

    if source_file == destination_file:
        return

    if not source_file.exists():
        command_log.warning(f'Unable to move \'{source_file}\', file does not exist')
        raise MoveCommandError(f'Unable to move \'{source_file}\', file does not exist')

    try:
        if not destination_file.parent.exists():
            destination_file.parent.mkdir(parents=True)

        source_file.replace(destination_file)

    except OSError as exception:
        command_log.warning(
            f'Unable to move \'{source_file}\' to \'{destination_file}\', {exception}'
        )
        raise MoveCommandError(
            f'Unable to move \'{source_file}\' to \'{destination_file}\', {exception}'
        )


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
