from PySide6 import QtCore as qtc
from ..classes import (
    DefaultThreadSignals,
    ErrorEnum
)
from ..functions import (
    scan_for_playlists,
    walkman_playlist_checker
)

class ScanMusicFolderThread(qtc.QRunnable):
    class ThreadSignals(DefaultThreadSignals):
        error = qtc.Signal(object)
        finished = qtc.Signal(list)

    def __init__(self, music_folder_path):
        super().__init__()
        self.music_folder_path = music_folder_path
        self.signals = self.ThreadSignals()

    @qtc.Slot()
    def run(self) -> None:
        try:
            self.signals.progress.emit(20)
            music_folder_info = scan_for_playlists(self.music_folder_path, walkman_playlist_checker, self.signals.progress)
            self.signals.progress.emit(100)
        except OSError:
            self.signals.error.emit(ErrorEnum.SCAN_FOLDER_ERROR)
        else:
            self.signals.finished.emit(music_folder_info)
