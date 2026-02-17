from PySide6 import (
    QtWidgets as qtw,
    QtCore as qtc,
)

class GenericFileSystemTreeView(qtw.QWidget):
    """
    Generic PySide6 TreeView for a file system with context menu.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = qtw.QVBoxLayout()
        self.setLayout(layout)

        self._model = qtw.QFileSystemModel()
        self._model.setRootPath(qtc.QDir.rootPath()) # the default

        self._tree_view = qtw.QTreeView()
        self._tree_view.setModel(self._model)
        self.setContextMenuPolicy(qtc.Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.context_menu)

        layout.addWidget(self._tree_view)

    def set_root_path(
            self,
            path: str,
            file_filters: list = None,
            hidden_columns: list = None,
            apply_filters_to_folders: bool = False) -> None:
        """
        Set the root path for the tree view.

        :param path: The new root path for the tree view.
        :param file_filters: What file filters to apply.
        :param hidden_columns: Which columns to hide in the tree view; defaults to None.
        :param apply_filters_to_folders: Have the filters apply to the folders; default False.
        """
        self._model.setRootPath(path)
        self._tree_view.setRootIndex(self._model.index(path))

        self._model.setNameFilterDisables(apply_filters_to_folders)

        if file_filters is not None:
            self._model.setNameFilters(file_filters)

        if hidden_columns is not None:
            for column in hidden_columns:
                self._tree_view.setColumnHidden(column, True)

    def context_menu(self, pos) -> None:
        # confirm the selection from the model is valid and the model had
        # initialized properly
        selection_model = self._tree_view.selectionModel()
        if not selection_model or not selection_model.hasSelection():
            return

        # confirm the index is valid (IE, the user clicked on an item)
        index = selection_model.currentIndex()
        if not index.isValid():
            return

        # Create menu with actions
        menu = qtw.QMenu()
        edit_action = menu.addAction("Edit")
        info_action = menu.addAction("Info")
        menu.addSeparator()
        delete_action = menu.addAction("Delete")

        if self._model.fileInfo(index).isFile():
            action = menu.exec_(self._tree_view.viewport().mapToGlobal(pos))
            item = self._model.fileInfo(index).path()

            if action == edit_action:
                print(f"Editing {item}")
            elif action == info_action:
                print(f"Info {item}")
            elif action == delete_action:
                print(f"Deleting {item}")
