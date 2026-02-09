from PySide6 import QtCore as qtc
from ..classes import DefaultThreadSignals
from ..functions import scan_music_folder, walkman_playlist_checker

class ScanMusicFolderThread(qtc.QRunnable):
    class ThreadSignals(DefaultThreadSignals):
        finished = qtc.Signal(object)

    def __init__(self, music_folder_path):
        super().__init__()
        self.music_folder_path = music_folder_path
        self.signals = self.ThreadSignals()

    @qtc.Slot()
    def run(self) -> None:
        try:
            music_folder_info = scan_music_folder(self.music_folder_path, walkman_playlist_checker)
        except OSError:
            self.signals.error.emit()
        except BaseException:
            self.signals.error.emit()
        else:
            self.signals.finished.emit(music_folder_info)
