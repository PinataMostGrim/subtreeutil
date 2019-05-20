import os
from pathlib import Path
import pytest
import stat
import shutil


import subtreeutil.command as command


TEST_FILE_1 = 'command_test_file_1.txt'
TEST_FOLDER_1 = 'command_test_folder_1'
TEST_FOLDER_2 = 'command_test_folder_2'


# Helper methods
def get_test_file_path():
    return Path(__file__).parent / TEST_FILE_1


def get_test_file_2_path():
    return Path(__file__).parent / TEST_FOLDER_1 / TEST_FILE_1


def get_test_file_3_path():
    return Path(__file__).parent / TEST_FOLDER_2 / TEST_FILE_1


def get_test_folder_path():
    return Path(__file__).parent / TEST_FOLDER_1


def get_test_folder_2_path():
    return Path(__file__).parent / TEST_FOLDER_2


def create_test_folder():
    folder = get_test_folder_path()
    folder.mkdir(parents=True, exist_ok=True)


def delete_test_folder():
    folder = get_test_folder_path()
    if folder.exists():
        shutil.rmtree(folder)


def set_test_folder_readonly():
    folder = get_test_folder_path()
    if folder.exists():
        os.chmod(folder, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)


def set_test_folder_writable():
    folder = get_test_folder_path()
    if folder.exists():
        os.chmod(folder, stat.S_IWUSR)


def create_test_folder_2():
    folder2 = get_test_folder_2_path()
    folder2.mkdir(parents=True, exist_ok=True)


def delete_test_folder_2():
    folder2 = get_test_folder_2_path()
    if folder2.exists():
        shutil.rmtree(folder2)


def create_test_file():
    file1 = get_test_file_path()
    file1.touch()


def delete_test_file():
    file = get_test_file_path()
    if file.exists():
        file.unlink()


def set_test_file_readonly():
    file = get_test_file_path()
    if file.exists():
        os.chmod(file, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)


def set_test_file_writable():
    file = get_test_file_path()
    if file.exists():
        os.chmod(file, stat.S_IWUSR)


def create_test_file_2():
    file2 = get_test_file_2_path()
    file2.touch()


def delete_test_file_2():
    file2 = get_test_file_2_path()
    if file2.exists():
        file2.unlink()


# Fixtures
@pytest.fixture
def fixture_folder():
    create_test_folder()
    yield 'fixture_folder'
    delete_test_folder()


@pytest.fixture
def fixture_folder_for_move():
    create_test_folder()
    create_test_file_2()
    yield 'fixture_folder_for_move'
    delete_test_folder()
    delete_test_folder_2()


@pytest.fixture
def fixture_folder_for_move_destination_exists():
    create_test_folder()
    create_test_file_2()
    create_test_folder_2()
    yield 'fixture_folder_for_move_destination_exists'
    delete_test_folder()
    delete_test_folder_2()


@pytest.fixture
def fixture_folder_with_contents():
    create_test_folder()
    create_test_file_2()
    yield 'fixture_folder_with_contents'
    delete_test_folder()


@pytest.fixture
def fixture_folder_readonly():
    create_test_folder()
    set_test_folder_readonly()
    yield 'fixture_folder_readonly'
    set_test_folder_writable()
    delete_test_folder()


@pytest.fixture
def fixture_file():
    create_test_file()
    yield 'fixture_file'
    delete_test_file()


@pytest.fixture
def fixture_file_for_move():
    create_test_file()
    yield "fixture_file_for_move"
    delete_test_file()
    # A successful move will place the test file inside test_folder.
    delete_test_folder()


@pytest.fixture
def fixture_readonly_file():
    create_test_file()
    set_test_file_readonly()
    yield "fixture_readonly_file"
    set_test_file_writable()
    delete_test_file()


# Tests
# move folder into location that already exists
# move readonly folder

def test_move_folder(fixture_folder_for_move):
    """ """
    source = get_test_folder_path()
    destination = get_test_folder_2_path()

    assert source.exists() is True
    assert destination.exists() is False

    command.move_folder(source, destination)

    assert source.exists() is False
    assert destination.exists() is True


def test_move_folder_destination_already_exists(fixture_folder_for_move_destination_exists):
    """Tests for moving a folder and its into an existing folder."""
    source = get_test_folder_path()
    destination = get_test_folder_2_path()
    file3 = get_test_file_3_path()

    assert source.exists() is True
    assert destination.exists() is True

    command.move_folder(source, destination)

    assert source.exists() is False
    assert destination.exists() is True
    assert file3.exists() is True


def test_delete_folder(fixture_folder):
    """Tests for the correct deletion of a folder."""
    folder = get_test_folder_path()
    command.delete_folder(folder)
    assert folder.exists() is False


def test_delete_folder_with_contents(fixture_folder_with_contents):
    """"""
    folder = get_test_folder_path()
    command.delete_folder(folder)
    assert folder.exists() is False


def test_delete_folder_missing():
    """Tests for raising an exception if attempting to delete a folder that doesn't exist."""
    folder = get_test_folder_path()
    with pytest.raises(command.DeleteCommandError):
        command.delete_folder(folder)


def test_delete_folder_readonly(fixture_folder_readonly):
    """Tests for raising an exception if attempting to delete a readonly folder."""
    folder = get_test_folder_path()
    with pytest.raises(command.DeleteCommandError):
        command.delete_folder(folder)


def test_move_file(fixture_file_for_move):
    """ """
    source = get_test_file_path()
    destination = get_test_file_2_path()

    assert source.exists() is True
    assert destination.exists() is False

    command.move_file(source, destination)

    assert source.exists() is False
    assert destination.exists() is True


def test_move_file_missing():
    """Test for raising an exception if attempting to delete a file that doesn't exist."""
    source = get_test_file_path()
    destination = get_test_file_2_path()

    with pytest.raises(command.MoveCommandError):
        command.move_file(source, destination)


def test_move_file_same_arguments(fixture_file):
    """Tests that giving identical arguments to move_file() leaves the file intact at
    the source location."""
    source = get_test_file_path()
    command.move_file(source, source)
    assert source.exists() is True


def test_delete_file(fixture_file):
    """Tests for the correct deletion of a file."""
    file = get_test_file_path()
    command.delete_file(file)
    assert file.exists() is False


def test_delete_file_readonly(fixture_readonly_file):
    """Test for raising an exception if attempting to delete a readonly file."""
    file = get_test_file_path()
    # print(f'User can access file: {os.access(file, os.W_OK)}')
    with pytest.raises(command.DeleteCommandError):
        command.delete_file(file)


def test_delete_file_missing():
    """Tests for raising an exception if attempting to delete a file that doens't exist."""
    file = get_test_file_path()
    with pytest.raises(command.DeleteCommandError):
        command.delete_file(file)
