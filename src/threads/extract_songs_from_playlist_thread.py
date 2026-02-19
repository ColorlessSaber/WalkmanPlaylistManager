from PySide6 import QtCore as qtc
from ..classes import (
    DefaultThreadSignals,
    ErrorEnum
)
from ..functions import extract_songs_from_playlist

class ExtractSongsFromPlaylistThread(qtc.QRunnable):
    class ThreadSignals(DefaultThreadSignals):
        error = qtc.Signal(object)
        finished = qtc.Signal(tuple)

    def __init__(self, name_of_playlist: str, path_to_playlist: str):
        super().__init__()
        self.name_of_playlist = name_of_playlist
        self.path_to_playlist = path_to_playlist
        self.signals = self.ThreadSignals()

    @qtc.Slot()
    def run(self) -> None:
        try:
            self.signals.progress.emit(20)
            songs_in_playlist = extract_songs_from_playlist(self.name_of_playlist, self.path_to_playlist)
            self.signals.progress.emit(100)
        except OSError:
            self.signals.error.emit(ErrorEnum.EXTRACT_SONGS_ERROR)
        except BaseException:
            self.signals.error.emit(ErrorEnum.EXTRACT_SONGS_ERROR)
        else:
            self.signals.finished.emit(songs_in_playlist)