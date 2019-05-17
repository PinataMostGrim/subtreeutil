"""Executes commands using the subprocess module.
"""

import logging
import subprocess


command_log = logging.getLogger('subtreeutil.command')


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

    process = subprocess.Popen(command,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)

    o, e = process.communicate()

    if display and o:
        command_log.info(o.decode('ascii'))
    else:
        command_log.debug(o.decode('ascii'))

    if e:
        command_log.error(e.decode('ascii'))

    return o.decode('ascii'), e.decode('ascii')
