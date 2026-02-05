from PySide6 import QtCore as qtc
from ..classes import DefaultThreadSignals

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
            print("hello", self.music_folder_path)
        except OSError:
            self.signals.error.emit()
        except BaseException:
            self.signals.error.emit()
        else:
            self.signals.finished.emit("hello")
