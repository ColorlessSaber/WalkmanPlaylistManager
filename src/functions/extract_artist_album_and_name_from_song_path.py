import pathlib

def extract_artist_album_and_name_from_song_path(song_dir_path: str) -> tuple[str, str, str]:
    """
    Extracts the artist, album, and song name from the directory path to the song.

    :param song_dir_path: Path to the song.
    :return: A tuple containing the artist, album, and song name.
    """
    path = pathlib.Path(song_dir_path)
    return path.parent.parent.name, path.parent.name, path.name