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
    with config_path.open(mode='w') as f:
        json.dump(get_default_config(), f, indent=4)


def get_default_config():
    return _DEFAULT_CONFIG.copy()


def load_config_file(config_path: Path):
    global _loaded_config

    # TODO: Try except here?
    with config_path.open('r') as f:
        _loaded_config = json.load(f)


def get_config():
    global _loaded_config
    if _loaded_config is None:
        return get_default_config()

    return _loaded_config


def get_remote_name():
    config = get_config()
    return config[_REMOTE_NAME]


def get_remote_url():
    config = get_config()
    return config[_REMOTE_URL]


def get_branch():
    config = get_config()
    return config[_BRANCH]


def get_source_paths():
    config = get_config()
    return config[_SOURCE_PATHS]


def get_destination_paths():
    config = get_config()
    return config[_DESTINATION_PATHS]


def get_cleanup_paths():
    config = get_config()
    return config[_CLEANUP_PATHS]
