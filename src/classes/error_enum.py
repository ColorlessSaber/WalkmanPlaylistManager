from enum import IntFlag, auto

class ErrorEnum(IntFlag):
    DELETE_PLAYLIST_ERROR = auto()
    SCAN_FOLDER_ERROR = auto()
    EXTRACT_SONGS_ERROR = auto()
    SAVE_PLAYLIST_ERROR = auto()