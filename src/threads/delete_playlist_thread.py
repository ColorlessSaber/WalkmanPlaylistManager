import pathlib
from PySide6 import QtCore as qtc
from classes import (
    DefaultThreadSignals,
    ErrorEnum
)

class DeletePlaylistThread(qtc.QRunnable):
    class ThreadSignals(DefaultThreadSignals):
        error = qtc.Signal(object)

    def __init__(self, playlist_name: str, directory: str):
        super().__init__()
        self.playlist_name = playlist_name
        self.directory = directory

        self.signals = self.ThreadSignals()

    @qtc.Slot()
    def run(self) -> None:
        try:
            self.signals.progress.emit(30)
            file_path = pathlib.Path(self.directory).joinpath(self.playlist_name + '.M3U8')
            self.signals.progress.emit(60)
            file_path.unlink()
            self.signals.progress.emit(100)
        except FileNotFoundError:
            self.signals.error.emit(ErrorEnum.DELETE_PLAYLIST_ERROR)
        else:
            self.signals.finished.emit()
