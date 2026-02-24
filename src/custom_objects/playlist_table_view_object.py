from PySide6 import (
    QtCore as qtc,
    QtWidgets as qtw
)
from .generic_pyside_objects import GenericTableView

class PlaylistTableView(GenericTableView):
    """
    The playlist table view
    """
    signal_remove_song = qtc.Signal(int)

    def context_menu(self, pos: qtc.QPoint) -> None:
        menu = qtw.QMenu()
        remove_song_action = menu.addAction("Remove Song")

        action = menu.exec_(self.mapToGlobal(pos))
        if action == remove_song_action:
            self.signal_remove_song.emit(self.indexAt(pos).row())
