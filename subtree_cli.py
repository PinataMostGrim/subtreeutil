"""
Command line interface for interacting with the subtree utility module. Automates
checking out and moving files and folders from a remote repository.

Usage:
- Create or edit a configuration file using the 'subtree config' command
- Perform a checkout operation using the 'subtree checkout' command and supplying a
configuration file
- Use the 'subtree -h' command for usage instructions.

Notes:
- A repository must already be present in the current working directory
- CLI application uses relative paths. It is best to run this script from a
repository's root folder.
- Configuration values for 'source_paths', 'destination_paths' and 'cleanup_paths'
can be files, folders, or a list containing a mix of either.
- When defining 'destination_paths', ensure the number of entries matches the number
of `source_paths`
"""

import argparse
from argparse import Namespace

import logging
import logging.config

from pathlib import Path

import sys

import subtreeutil.core as core
import subtreeutil.config as config


class Command:
    """Base command class."""
    def execute(self, args: Namespace):
        """Executes the command.

        Args:
          args: Namespace: Namespace object containing arguments for the command.
        """
        pass

    @staticmethod
    def configure(subparser):
        """Add additional arguments to the command's subparser.

        Args:
          subparser: A Subparser object to configure.
        """
        pass


class Checkout(Command):
    def execute(self, args):
        """Executes a full checkout command using a configuration file.

        Args:
          args: A Namespace object containing a parsed argument for the configuration
          file to load.
        """
        config_path = Path(args.file)

        print('')
        core.perform_checkout(config_path)

    @staticmethod
    def configure(subparser):
        subparser.add_argument('file', type=str, help='Configuration file to use for checkout operation')


class EditConfig(Command):
    def execute(self, args):
        """Executes a configuration file edit command.

        Args:
          args: A Namespace object containing a parsed argument for the configuration
          file to edit.
        """
        config_path = Path(args.file)

        print('')
        config.edit_config_file(config_path)
        print('')

    @staticmethod
    def configure(subparser):
        subparser.add_argument('file', type=str, help='The configuration file to edit')


def main():
    """Gathers system arguments, parses them, and executes the requested command."""
    args = get_args(sys.argv[1:])
    command = args.command()
    command.execute(args)


def get_args(argv):
    """Builds a Namespace object with parsed arguments.

    Args:
      argv: A list of arguments to parse.

    Returns:
        A Namespace object containing parsed arguements.
    """
    parser = argparse.ArgumentParser(
        prog='subtree_cli',
        description='Application that automates checking out files and folders from a remote subtree.')

    subparsers = parser.add_subparsers(title='Commands')

    checkout_parser = subparsers.add_parser('checkout', help='Perform a checkout operation using the specified configuration file')
    Checkout.configure(checkout_parser)
    checkout_parser.set_defaults(command=Checkout)

    config_parser = subparsers.add_parser('config', help='Edit the specified configuration file')
    EditConfig.configure(config_parser)
    config_parser.set_defaults(command=EditConfig)

    args = parser.parse_args(argv)
    if 'command' not in args:
        parser.print_help()
        sys.exit(2)

    return args


def configure_log():
    """Configures subtreeutil's logging. The log file will be created in a log folder as
    a sibling of this script.
    """

    log_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "style": "{",
                "format": "{levelname}:{name}:{message}"
            },
            "display": {
                "style": "{",
                "format": "{message}"
            },
            "timestamp": {
                "style": "{",
                "format": "[{asctime}][{levelname}] {name}: {message}"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stderr",
                "formatter": "display"
            },
            "file": {
                "class": "logging.FileHandler",
                "filename": "",
                "formatter": "timestamp"
            },
        },
        "loggers": {
            "subtreeutil.core": {
                "handlers": ["console", "file"]
            },
            "subtreeutil.config": {
                "handlers": ["console", "file"]
            },
            "subtreeutil.command": {
                "handlers": ["console", "file"]
            }
        },
        "root": {
            "level": "INFO"
        }
    }

    cli_path = Path(__file__).parent
    log_path = cli_path / 'logs' / 'subtree_cli.log'

    if not log_path.parent.exists():
        log_path.parent.mkdir(parents=True)

    log_config['handlers']['file']['filename'] = log_path
    logging.config.dictConfig(log_config)


if __name__ == '__main__':
    configure_log()
    main()
    logging.shutdown()
