from PySide6 import (
    QtWidgets as qtw,
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

    # *** Main Window Methods ***
    def closeEvent(self, event) -> None:
        """
        Close the application gracefully.
        """
        response = qtw.QMessageBox.question(
            self,
            'Close Application?',
            'Are you sure you want to close the application?',
            buttons=qtw.QMessageBox.StandardButton.Yes | qtw.QMessageBox.StandardButton.No,
            defaultButton=qtw.QMessageBox.StandardButton.Yes
        )

        if response == qtw.QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()