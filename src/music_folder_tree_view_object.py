from PySide6 import (
    QtCore as qtc,
    QtWidgets as qtw
)
from custom_objects import GenericFileSystemTreeView
import pathlib

class MusicFolderTreeView(GenericFileSystemTreeView):
    """
    The music folder tree view
    """

    signal_song_to_add = qtc.Signal(tuple)

    def context_menu(self, pos: qtc.QPoint) -> None:
        # confirm the selection from the model is valid and the model had
        # initialized properly
        selection_model = self._tree_view.selectionModel()
        if not selection_model or not selection_model.hasSelection():
            return

        # confirm the index is valid (IE, the user clicked on an item)
        index = selection_model.currentIndex()
        if not index.isValid():
            return

        menu = qtw.QMenu()
        add_song_to_playlist_action = menu.addAction("Add Song to Playlist")

        if self._model.fileInfo(index).isFile():
            action = menu.exec_(self.mapToGlobal(pos))

            if action == add_song_to_playlist_action:
                path = pathlib.Path(self._model.filePath(index))
                self.signal_song_to_add.emit((path.parent.parent.name, path.parent.name, path.name))
