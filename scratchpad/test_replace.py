from pathlib import Path
from shutil import rmtree


SOURCE = 'Tests\\Source'
SOURCE_CLEANUP = 'Tests\\Source'

DESTINATION = 'Tests\\Destination\\Source'
# DESTINATION = 'Tests'
DESTINATION_CLEANUP = 'Tests\\Destination'


def setup():
    print('Creating test files...')

    for i in range(5):
        file = Path('{}\\file{}.txt'.format(SOURCE, i))
        create_file(file)

    for i in range(5, 11):
        file = Path('{}\\something\\file{}.txt'.format(SOURCE, i))
        create_file(file)


def create_file(file: Path):
    if not file.parent.exists():
        file.parent.mkdir(parents=True)
    file.touch(exist_ok=True)


def cleanup_source():
    print('Removing source folders...')

    rmtree(SOURCE_CLEANUP, ignore_errors=True)


def cleanup_full():
    print('Removing all test folders...')

    rmtree(SOURCE_CLEANUP, ignore_errors=True)
    rmtree(DESTINATION_CLEANUP, ignore_errors=True)


def move_source_folder():
    print('Moving source files to \'{}\''.format(DESTINATION_CLEANUP))

    source = Path(SOURCE)
    destination = Path(DESTINATION)

    if not destination.exists():
        destination.parent.mkdir(parents=True, exist_ok=True)

    source.replace(destination)


def move_files():
    print('Moving files...')

    source = Path(SOURCE)

    for file in source.rglob('*'):
        source_file = Path(file)

        if source_file.is_dir():
            continue

        destination_file = Path(DESTINATION) / source_file.relative_to(SOURCE)

        print(f'{source_file} -> {destination_file}')

        if not destination_file.parent.exists():
            destination_file.parent.mkdir(parents=True)

        source_file.replace(destination_file)


setup()
move_files()
cleanup_source()
