from PySide6 import (
    QtWidgets as qtw,
)

from .view import View
from .model import Model

class MainWindow(qtw.QMainWindow):
    """The main window for the application"""

    def __init__(self):
        super().__init__()

        self.view = View()
        self.model = Model()
        self.setCentralWidget(self.view)
        self.setMinimumSize(
            800, # width
            600  # height
        )
        self.setWindowTitle("Walkman Playlist Manager")

        # view signals that connect to the model slots
        self.view.signal_initiate_scan_of_music_folder.connect(self.model.start_scan_of_music_folder_thread)
        self.view.signal_initiate_scan_of_playlist.connect(self.model.read_in_playlist)

        # model signals that connect to the view slots
        self.model.signal_analysis_of_music_folder.connect(self.view.update_screen_information)
        self.model.signal_analysis_of_playlist.connect(self.view.update_playlist_table)
        self.model.signal_update_progress.connect(self.view.update_progress_bar)
        self.model.signal_error_message.connect(self.view.messagebox_system_error_detected)

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