import re, pathlib

def extract_songs_from_playlist(name_of_playlist: str, playlist_directory_path: str) -> tuple:
    """
    Opens the playlist; reads the songs in the playlist; and save each song in a list where each entry is
    the song's artist, album, and name.

    :param name_of_playlist: Name of the playlist.
    :param playlist_directory_path: Path to the playlist.
    :return: A tuple of the songs in the playlist, each entry is a tuple (artist, album, name).
    """
    playlist_markers = re.compile(r"^#EXT\w+")  # markers used in Walkman playlists
    full_playlist_path = str(pathlib.Path(playlist_directory_path).joinpath(name_of_playlist)) + '.M3U8'
    with open(full_playlist_path, "r") as file:
        clean_list_of_songs = [line_item.strip() for line_item in file.readlines()
                               if not playlist_markers.match(line_item)]
    broken_down_list_of_songs = [tuple(song.split('/')) for song in clean_list_of_songs]
    return tuple(broken_down_list_of_songs)