def walkman_playlist_checker(file_to_check: str) -> bool:
    """
    Checks to see if the given file is a valid Walkman music playlist.
    Does this by checking two things:
    1) files is a .M3U8 file
    2) does not start with a '._'

    :param file_to_check: the file name to validate
    :return: True if the file is a valid Walkman music playlist, False otherwise
    """
    if file_to_check.endswith(".M3U8") and not file_to_check.startswith("._"):
        return True
    else:
        return False

