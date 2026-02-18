from PySide6 import QtCore as qtc
from ..classes import DefaultThreadSignals
from ..functions import generate_playlist

class SavingPlaylistThread(qtc.QRunnable):
    class ThreadSignals(DefaultThreadSignals):
        """Default signals for thread"""

    def __init__(self, list_of_songs: list, name_of_playlist: str, save_location: str) -> None:
        super().__init__()
        self.list_of_songs = list_of_songs
        self.name_of_playlist = name_of_playlist
        self.save_location = save_location

        self.signals = self.ThreadSignals()

    @qtc.Slot()
    def run(self) -> None:
        try:
            self.signals.progress.emit(20)
            generate_playlist(self.list_of_songs, self.name_of_playlist, self.save_location)
            self.signals.progress.emit(100)
        except OSError:
            self.signals.error.emit()
        else:
            self.signals.finished.emit()