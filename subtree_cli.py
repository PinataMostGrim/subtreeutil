"""
Command line interface for interacting with the subtree utility module. Automates checking out and moving files and folders from a remote repository.

Usage:
- Create or edit a configuration file using the 'subtree config' command
- Perform a checkout operation using the 'subtree checkout' command and supplying a configuration file
- Use the 'subtree -h' command for usage instructions.

Notes:
- CLI application uses relative paths. It is best to run this script from the repository's root folder.
- Configuration values for 'source_paths', 'destination_paths' and 'cleanup_paths' can be files, folders, or a list containing a mix of either.
- When defining 'destination_paths', ensure the number of entries matches the number of `source_paths`
"""

import argparse
from argparse import Namespace

from pathlib import Path

import sys
import subtreeutil.core as sutil


from subtreeutil import config as configuration


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
          args: A Namespace object containing a parsed argument for the configuration file to load.
        """
        config_path = Path(args.file)

        if not config_path.exists():
            print(f'Unable to find configuration file \'{config_path}\'')
            return

        sutil.perform_checkout(config_path)

    @staticmethod
    def configure(subparser):
        subparser.add_argument('file', type=str, help='Configuration file to use for checkout operation')


class EditConfig(Command):
    def execute(self, args):
        """Executes a configuration file edit command.

        Args:
          args: A Namespace object containing a parsed argument for the configuration file to edit.
        """
        config_path = Path(args.file)
        configuration.edit_config_file(config_path)

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


if __name__ == '__main__':
    main()
