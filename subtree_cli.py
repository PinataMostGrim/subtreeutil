'''
Automates checking out and moving files and folders from a remote repository.

Usage:
- Create and edit a configuration file using the 'config' command
- Perform a checkout operation using the 'checkout' command and supplying a configuration file

Notes:
- Uses relative paths. It is best to run this script from the repository's root folder.
- 'source_paths', 'destination_paths' and 'cleanup_paths' can be files, folders, or a list containing either or both.
- When defining 'destination_paths', ensure the number of entries matches the number of `source_paths`
'''

import argparse
from argparse import Namespace

from pathlib import Path

import sys
import subtreeutil.subtreeutil as sutil


from subtreeutil import config as configuration


class Command:
    def execute(self, options: Namespace):
        pass

    @staticmethod
    def configure(subparser):
        pass


class Checkout(Command):
    def execute(self, options):
        config_path = Path(options.file)

        if not config_path.exists():
            print(f'Unable to find configuration file \'{config_path}\'')
            return

        sutil.perform_checkout(config_path)

    @staticmethod
    def configure(subparser):
        subparser.add_argument('file', type=str, help='Configuration file to use for checkout operation')


class EditConfig(Command):
    def execute(self, options):
        config_path = Path(options.file)
        configuration.edit_config_file(config_path)

    @staticmethod
    def configure(subparser):
        subparser.add_argument('file', type=str, help='The configuration file to edit')


def main():
    options = get_options(sys.argv[1:])
    command = options.command()
    command.execute(options)


def get_options(argv):
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


    options = parser.parse_args(argv)
    if 'command' not in options:
        parser.print_help()
        sys.exit(2)

    return options


if __name__ == '__main__':
    main()
