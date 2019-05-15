import json
import os
import subprocess

from pathlib import Path

# Config variable names
_REMOTE_NAME = 'remote_name'
_REMOTE_URL = 'remote_url'
_BRANCH = 'branch'
_SOURCE_PATHS = 'source_paths'
_DESTINATION_PATHS = 'destination_paths'
_CLEANUP_PATHS = 'cleanup_paths'

# Default configuration values
_DEFAULT_CONFIG = {
    _REMOTE_NAME: 'subtree',
    _REMOTE_URL: '',
    _BRANCH: 'develop',
    _SOURCE_PATHS: [],
    _DESTINATION_PATHS: [],
    _CLEANUP_PATHS: []
}


_loaded_config = None


def edit_config_file(config_path: Path):
    """Opens the specified configuration file with the system's default editor.
    """
    if not config_path.suffix == '.json':
        config_path = config_path.with_suffix('.json')

    if not config_path.exists():
        # TODO: Log event
        create_config_file(config_path)

    try:
        # Windows
        os.startfile(str(config_path))
    except AttributeError:
        # OSX / Linux
        subprocess.Popen(['open', str(config_path)])


def create_config_file(config_path: Path):
    """Creates a configuration file with default values at the specified path.
    """
    # Try exception here?
    with config_path.open(mode='w') as f:
        json.dump(get_default_config(), f, indent=4)


def get_default_config():
    """Fetches a copy of the default configuration dictionary.
    """
    return _DEFAULT_CONFIG.copy()


def load_config_file(config_path: Path):
    """Loads a configuration file into the loaded configuration global dictionary.
    """
    global _loaded_config

    # TODO: Try catch here
    # TODO: Try except here?
    with config_path.open('r') as f:
        _loaded_config = json.load(f)

    # TODO: Validate config file here


def get_config():
    """Fetches the loaded configuration dictionary.

    Returns:
        The global dictionary storing a mapping configuration keys to values.
    """
    global _loaded_config
    if _loaded_config is None:
        return get_default_config()
        # TODO: Log event

    return _loaded_config


def get_remote_name():
    """Fetches remote repository name from the loaded configuration.
    """
    config = get_config()
    return config[_REMOTE_NAME]


def get_remote_url():
    """Fetches remote repository url from the loaded configuration.
    """
    config = get_config()
    return config[_REMOTE_URL]


def get_branch():
    """Fetches remote repository branch name from the loaded configuration.
    """
    config = get_config()
    return config[_BRANCH]


def get_source_paths():
    """Fetches source paths from the loaded configuration.
    """
    config = get_config()
    return config[_SOURCE_PATHS]


def get_destination_paths():
    """Fetches destination paths from the loaded configuration.
    """
    config = get_config()
    return config[_DESTINATION_PATHS]


def get_cleanup_paths():
    """Fetches cleanup paths from the loaded configuration.
    """
    config = get_config()
    return config[_CLEANUP_PATHS]
