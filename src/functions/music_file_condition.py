def music_file_condition(file: str) -> bool:
    """
    Validates that the given file is a music file

    :param file: the file to validate
    :return: True if file is a music file, False otherwise
    """
    if any(file.endswith(file_extension) for file_extension in [".mp3", ".wav", ".m4a", ".flac"]):
        return True
    else:
        return False