'''
Automates checking out and relocating specific folders from a remote repository.

Notes:
- Uses relative paths. This script is best to be run from the repository's root folder.
- Can only checkout a folder, files aren't supported yet.
'''

import subtreeutil.utility as sutil

from pathlib import Path


REMOTE_URL = ''

BRANCH = 'develop'
CHECKOUT_SOURCE = ''
CHECKOUT_DESTINATION = 

CLEANUP = ''


def main():
    sutil.add_subtree(REMOTE_URL)
    sutil.fetch_subtree()
    sutil.checkout_subtree_folder(BRANCH, CHECKOUT_SOURCE)
    sutil.unstage_all()
    sutil.remove_subtree()
    sutil.move_folder(
        Path(CHECKOUT_SOURCE),
        Path(CHECKOUT_DESTINATION))
    sutil.delete_folder(Path(CLEANUP))


if __name__ == '__main__':
    main()
