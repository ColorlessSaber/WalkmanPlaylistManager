import pathlib
from typing import Callable
from PySide6 import QtCore as qtc

def scan_for_playlists(
        music_folder_dir_path: str,
        playlist_file_condition: Callable[..., bool],
        progress_signal: qtc.Signal) -> list:
    """
    Takes the given directory path, find playlists in the folder, and return them in a list.

    :param music_folder_dir_path: Path to the music folder directory.
    :param playlist_file_condition: Function to check if the file is a valid playlist.
    :param progress_signal: Signal to report the progress status.
    :return: list of playlist(s)
    """
    progress_signal.emit(40)

    playlists_found = [entry.name for entry in pathlib.Path(music_folder_dir_path).iterdir() if entry.is_file() and playlist_file_condition(entry.name)]

    progress_signal.emit(60)

    return playlists_found