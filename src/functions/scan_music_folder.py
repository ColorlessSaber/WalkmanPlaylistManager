import os
from typing import Callable

def scan_music_folder(
        music_folder_dir_path: str,
        playlist_file_condition: Callable[..., bool]) -> dict:
    """
    Takes the given music_folder_dir_path and returns the folders and playlists found in it.

    :param music_folder_dir_path: Path to the music folder directory.
    :param playlist_file_condition: Function to check if the file is a valid playlist.
    :return: Dictionary of folders and playlists.
    """
    playlists_and_music_folders = {
        'playlists': [],
        'music_folders': [],
    }

    with os.scandir(music_folder_dir_path) as directory_iterator:
        for entry in directory_iterator:
            if entry.is_file() and playlist_file_condition(entry.name):
                playlists_and_music_folders['playlists'].append(entry.name)
            elif entry.is_dir():
                playlists_and_music_folders['music_folders'].append(entry.name)

    return playlists_and_music_folders