import pathlib

def generate_playlist(song_list: list, playlist_name: str, directory_path: str) -> None:
    """
    Generate a playlist in the specified directory and filled with the songs in the provided list.

    :param song_list: The list of songs to put in the playlist
    :param playlist_name: The name of the playlist
    :param directory_path: The directory where the playlist is stored
    :return:
    """
    # Create a new playlist with .M3U8 extension. if playlist already exist, override the contents
    # with the new additions/changes.
    with open(pathlib.Path(directory_path).joinpath(playlist_name + ".M3U8"), "wt") as file:

    # A Sony Walkman playlist has the following structure:
    #
    # #EXTM3U
    # #EXTINF:,
    # artist/album/song_with_extension
    # #EXTINF:,
    # ...
    # #EXTINF:,
    # artist/album/song_with_extension (The last song in playlist)
    #
    # The following code generates this structure.
        file.write("#EXTM3U\n")
        for song in song_list:
            artist, album, track = song
            file.write(f"#EXTINF:,\n{artist}/{album}/{track}\n")
