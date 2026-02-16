from PySide6 import (
    QtWidgets as qtw,
    QtCore as qtc
)

class GenericTableView(qtw.QTableView):
    """
    Generic PySide Table View with default context menu request.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setContextMenuPolicy(qtc.Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.context_menu)

    def context_menu(self, pos: qtc.QPoint) -> None:
        """
        Returns the context menu item for the given position.
        """
        # Create menu with actions
        menu = qtw.QMenu()
        edit_action = menu.addAction("Edit Cell")
        delete_action = menu.addAction("Delete Row")
        menu.addSeparator()
        print_value = menu.addAction("Print Value")

        # Show the menu at the right-click position
        action = menu.exec_(self.mapToGlobal(pos))

        if action == edit_action:
            row, col = self.indexAt(pos).row(), self.indexAt(pos).column()
            print(f"\"Editing\" cell at row {row}, column {col}")
        elif action == delete_action:
            row, col = self.indexAt(pos).row(), self.indexAt(pos).column()
            print(f"\"Deleting\" row {row}, column {col}")
        elif action == print_value:
            data = self.indexAt(pos).data()
            print(f"Data in cell {data}")