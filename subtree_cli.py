'''
Automates checking out and relocating specific folders from a remote repository.

Notes:
- Uses relative paths. This script is best to be run from the repository's root folder.
- Can only checkout a folder, files aren't supported yet.
'''

import subtree.subtree as subtree

from pathlib import Path


REMOTE_URL = ''

BRANCH = 'develop'
CHECKOUT_SOURCE = ''
CHECKOUT_DESTINATION = 

CLEANUP = ''


def main():
    subtree.add_subtree(REMOTE_URL)
    subtree.fetch_subtree()
    subtree.checkout_subtree_folder(BRANCH, CHECKOUT_SOURCE)
    subtree.unstage_all()
    subtree.remove_subtree()
    subtree.move_folder(
        Path(CHECKOUT_SOURCE),
        Path(CHECKOUT_DESTINATION))
    subtree.delete_folder(Path(CLEANUP))


if __name__ == '__main__':
    main()
