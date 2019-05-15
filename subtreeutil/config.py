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


def load_config(config: Path):
    # TODO: Try except here?
    with config.open('r') as f:
        data = json.load(f)

    return data


def edit_config(config: Path):
    if not config.suffix == '.json':
        config = config.with_suffix('.json')

    if not config.exists():
        create_default_config(config)

    try:
        # Windows
        os.startfile(str(config))
    except AttributeError:
        # OSX / Linux
        subprocess.Popen(['open', str(config)])


def create_default_config(config: Path):
    with config.open(mode='w') as f:
        json.dump(_DEFAULT_CONFIG, f, indent=4)
