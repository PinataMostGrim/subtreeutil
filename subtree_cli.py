'''
Automates checking out and moving folders from a remote repository.

Notes:
- Uses relative paths. This script is best to be run from the repository's root folder.
- Can only checkout a folder, files aren't supported yet.
'''

import argparse
import subtreeutil.utility as sutil
import sys

from argparse import Namespace
from pathlib import Path


class Command:
    def execute(self, options: Namespace):
        pass

    @staticmethod
    def configure(subparser):
        pass


class Checkout(Command):
    def execute(self, options):
        config_path = Path(options.config_file)

        if not config_path.exists():
            print(f'Unable to find {config_path}')
            return

        config = sutil.load_config(config_path)
        sutil.perform_checkout(config)

    @staticmethod
    def configure(subparser):
        subparser.add_argument('config_file', type=str, help='Configuration file to use for checkout operation')


class EditConfig(Command):
    def execute(self, options):
        config_path = Path(options.config_file)
        sutil.edit_config(config_path)

    @staticmethod
    def configure(subparser):
        subparser.add_argument('config_file', type=str, help='Name of the json configuration file to edit')


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

    edit_config = subparsers.add_parser('config', help='Edit the specified configuration file')
    EditConfig.configure(edit_config)
    edit_config.set_defaults(command=EditConfig)

    options = parser.parse_args(argv)
    if 'command' not in options:
        parser.print_help()
        sys.exit(2)

    return options


if __name__ == '__main__':
    main()
