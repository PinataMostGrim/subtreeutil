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


class ConfigurationError(Exception):
    """Base error for configuration Errors.
    """


class InvalidConfigurationError(ConfigurationError):
    """An error occurred while loading a configuration file.
    """
    pass


class EmptyConfigurationError(ConfigurationError):
    """An error occurred because configuration values were accessed before a configuration was loaded.
    """
    pass


def edit_config_file(config_path: Path):
    """Opens the specified configuration file with the system's default editor.
    """
    if not config_path.suffix == '.json':
        config_path = config_path.with_suffix('.json')

    if not config_path.exists():
        # TODO: Log event
        create_config_file(config_path)

    try:
        # Open file in Windows
        os.startfile(str(config_path))
    except AttributeError:
        # Open file in OSX / Linux
        subprocess.Popen(['open', str(config_path)])


def create_config_file(config_path: Path):
    """Creates a configuration file with default values at the specified path.
    """
    with config_path.open(mode='w') as f:
        json.dump(get_default_config(), f, indent=4)


def get_default_config():
    """Fetches a copy of the default configuration dictionary.
    """
    return _DEFAULT_CONFIG.copy()


def load_config_file(config_path: Path):
    """Loads a configuration file into the loaded configuration global dictionary.

    Raises:
        FileNotFoundError: An error occured while attempting to load a configuration file.
        InvalidConfigurationError: The specified configuration file is not valid.
    """
    global _loaded_config

    try:
        with config_path.open('r') as f:
            configuration = json.load(f)
    except FileNotFoundError:
        # TODO: Log event
        raise FileNotFoundError

    if validate_configuration(configuration):
        _loaded_config = configuration
    else:
        raise InvalidConfigurationError


def validate_configuration(configuration):
    default_config = get_default_config()
    is_valid_config = True

    for key, value in default_config.items():
        try:
            configuration[key]
        except KeyError:
            # TODO: Log event instead of printing it
            print(f'Configuration is missing key \'{key}\'')
            is_valid_config = False

    return is_valid_config


def get_config():
    """Fetches the loaded configuration dictionary.

    Returns:
        The global dictionary storing a mapping configuration keys to values.

    Raises:
        EmptyConfigurationError: A configuration value is accessed without a configuration file being loaded first.
    """
    global _loaded_config
    if _loaded_config is None:
        # TODO: Log event
        raise EmptyConfigurationError

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
