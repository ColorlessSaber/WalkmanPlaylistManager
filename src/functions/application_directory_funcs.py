"""
Containing functions that created, modified, and manage files in the application directory.
"""
from platformdirs import user_data_dir
from pathlib import Path
import logging


APP_NAME = "Walkman Playlist Manager"
APP_AUTHOR = "Walkman Playlist Manager"
LOGGER_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

def build_app_directory():
    """
    Builds the application directory folder structure.
    """
    data_dir = Path(user_data_dir(APP_NAME, APP_AUTHOR))
    logs_dir = data_dir / 'logs'
    data_dir.mkdir(parents=True, exist_ok=True)
    logs_dir.mkdir(exist_ok=True)

def setup_logger() -> None:
    """
    Gets the logger all setup for use within the application
    """
    data_dir = Path(user_data_dir(APP_NAME, APP_AUTHOR))
    logs_dir = data_dir / 'logs'

    logging.basicConfig(
        filename=logs_dir / 'app.log',
        level=logging.INFO,
        format=LOGGER_FORMAT,
    )
