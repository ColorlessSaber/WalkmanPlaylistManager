"""
Containing functions that created, modified, and manage files in the application directory.
"""
from platformdirs import user_data_dir
from pathlib import Path
import logging
import json

#TODO add in code to check version number of json file and migrate to newer format if necessary
APP_NAME = "Walkman Playlist Manager"
APP_AUTHOR = "Walkman Playlist Manager"
LOGGER_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

def build_app_directory():
    """
    Builds the application directory folder structure.

    :return: None
    """
    data_dir = Path(user_data_dir(APP_NAME, APP_AUTHOR))
    logs_dir = data_dir / 'logs'
    data_dir.mkdir(parents=True, exist_ok=True)
    logs_dir.mkdir(exist_ok=True)

def setup_app_logger(logging_level: int = logging.ERROR) -> None:
    """
    Gets the logger all setup for use within the application

    :param logging_level: The logging level to use
    :return: None
    """
    data_dir = Path(user_data_dir(APP_NAME, APP_AUTHOR))
    logs_dir = data_dir / 'logs'

    logging.basicConfig(
        filename=logs_dir / 'app.log',
        level=logging_level,
        format=LOGGER_FORMAT,
    )

def setup_app_settings_file() -> None:
    """
    Creates the settings json file for the application. Will skip process if file already exists.

    :return: None
    """
    data_dir = Path(user_data_dir(APP_NAME, APP_AUTHOR))
    settings_file = data_dir / 'settings.json'
    if not settings_file.exists():
        default_settings_dict = {
            "version": "1.1.0",
            "preferences": {
                "logging_settings": {
                    "level": logging.ERROR,
                }
            }
        }
        save_app_settings(default_settings_dict)

def load_app_settings() -> dict:
    """
    Loads the settings json file from the application directory.

    :return: dict
    """
    data_dir = Path(user_data_dir(APP_NAME, APP_AUTHOR))
    settings_file = data_dir / 'settings.json'
    with open(settings_file) as json_file:
        return json.load(json_file)

def save_app_settings(settings: dict) -> None:
    """
    Saves the new settings the user selected to the json file in the application directory.

    :param settings: The new settings to save
    :return: None
    """
    data_dir = Path(user_data_dir(APP_NAME, APP_AUTHOR))
    settings_file = data_dir / 'settings.json'
    with open(settings_file, 'w') as json_file:
        json.dump(settings, json_file, indent=2)

def delete_then_recreate_log_file() -> None:
    """
    Deletes the log files located in the application directory, and then creates a new one.
    """
    data_dir = Path(user_data_dir(APP_NAME, APP_AUTHOR))
    log_file = data_dir / 'logs/app.log'
    log_file.unlink()
    log_file.touch()
