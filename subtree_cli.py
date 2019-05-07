'''
Automates checking out and relocating specific folders from a remote repository.

Notes:
- Uses relative paths. This script is best to be run from the repository's root folder.
- Can only checkout a folder, files aren't supported yet.
'''

import argparse
import subtreeutil.utility as sutil
import sys

from argparse import Namespace
from pathlib import Path


REMOTE_URL = ''

BRANCH = 'develop'
CHECKOUT_SOURCE = ''
CHECKOUT_DESTINATION = 

CLEANUP = ''


class Command:
    def execute(self, options: Namespace):
        pass

    @staticmethod
    def configure(subparser):
        pass


class EditConfig(Command):
    def execute(self, options):
        config_path = Path(options.config_file)
        sutil.edit_config(config_path)

    @staticmethod
    def configure(subparser):
        subparser.add_argument('config_file', type=str, help='Name of the json configuration file to edit')


class Test(Command):
    def execute(self, options):
        sutil.add_subtree(REMOTE_URL)
        sutil.fetch_subtree()
        sutil.checkout_subtree_folder(BRANCH, CHECKOUT_SOURCE)
        sutil.unstage_all()
        sutil.remove_subtree()
        sutil.move_folder(
            Path(CHECKOUT_SOURCE),
            Path(CHECKOUT_DESTINATION))
        sutil.delete_folder(Path(CLEANUP))

    @staticmethod
    def configure(subparser):
        pass


def main():
    options = get_options(sys.argv[1:])
    command = options.command()
    command.execute(options)


def get_options(argv):
    parser = argparse.ArgumentParser(
        prog='subtree_cli',
        description='Application that automates checking out files and folders from a remote subtree.')

    subparsers = parser.add_subparsers(title='Commands')

    edit_config = subparsers.add_parser('config', help='Edit the specified configuration file')
    EditConfig.configure(edit_config)
    edit_config.set_defaults(command=EditConfig)

    testParser = subparsers.add_parser('test', help='Test command')
    Test.configure(testParser)
    testParser.set_defaults(command=Test)

    options = parser.parse_args(argv)
    if 'command' not in options:
        parser.print_help()
        sys.exit(2)

    return options


if __name__ == '__main__':
    main()
