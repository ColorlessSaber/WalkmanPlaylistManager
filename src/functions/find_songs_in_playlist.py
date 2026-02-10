import re

def find_songs_in_playlist(playlist_directory_path: str) -> tuple:
    """
    Opens the playlist; reads the songs in the playlist; and save each song in a list where each entry is
    the song's artist, album, and name.

    :param playlist_directory_path: Path to the playlist.
    :return: A tuple of the songs in the playlist, each entry is a tuple (artist, album, name).
    """
    playlist_markers = re.compile(r"^#EXT\w+")  # markers used in Walkman playlists
    with open(playlist_directory_path, "r") as file:
        clean_list_of_songs = [line_item.strip() for line_item in file.readlines()
                               if not playlist_markers.match(line_item)]
    broken_down_list_of_songs = [tuple(song.split('/')) for song in clean_list_of_songs]
    return tuple(broken_down_list_of_songs)