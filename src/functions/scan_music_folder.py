import pathlib
from typing import Callable
from PySide6 import QtCore as qtc

def scan_music_folder(
        music_folder_dir_path: str,
        playlist_file_condition: Callable[..., bool],
        progress_signal: qtc.Signal) -> dict:
    """
    Takes the given music_folder_dir_path and returns the folders and playlists found in it.

    :param music_folder_dir_path: Path to the music folder directory.
    :param playlist_file_condition: Function to check if the file is a valid playlist.
    :param progress_signal: Signal to report the progress status.
    :return: Dictionary of folders and playlists.
    """
    playlists_and_music_folders = {
        'playlists': [],
        'music_folders': [],
    }
    progress_signal.emit(40)
    for entry in pathlib.Path(music_folder_dir_path).iterdir():
        if entry.is_file() and playlist_file_condition(entry.name):
            playlists_and_music_folders['playlists'].append(entry.name)
        elif entry.is_dir():
            playlists_and_music_folders['music_folders'].append(entry.name)
    progress_signal.emit(60)
    return playlists_and_music_folders