from PySide6 import (
    QtWidgets as qtw,
    QtCore as qtc,
    QtGui as qtg,
)

from .view import View

class MainWindow(qtw.QMainWindow):
    """The main window for the application"""

    def __init__(self):
        super().__init__()

        self.view = View()
        self.setCentralWidget(self.view)
        self.setMinimumSize(
            800, # width
            600  # height
        )
        self.setWindowTitle("Walkman Playlist Manager")

        self.show()