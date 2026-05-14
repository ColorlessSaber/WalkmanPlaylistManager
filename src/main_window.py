from PySide6 import (
    QtWidgets as qtw,
)

from .view import View
from .model import Model
from .pop_up_windows import ApplicationPreferencesWindow


class MainWindow(qtw.QMainWindow):
    """The main window for the application"""

    def __init__(self):
        super().__init__()

        # set up the model and view
        self.view = View()
        self.model = Model()
        self.setCentralWidget(self.view)
        self.setMinimumSize(
            1600, # width
            1200  # height
        )
        self.setWindowTitle("Walkman Playlist Manager")

        # setup menu bar
        menubar = qtw.QMenuBar()

        main_menu = menubar.addMenu("Walkman Playlist Manager")
        main_menu.addAction("Preferences...", self.open_preferences_window)

        self.setMenuBar(menubar)

        # view signals that connect to the model slots
        self.view.signal_initiate_scan_of_music_folder.connect(self.model.start_scan_of_music_folder_thread)
        self.view.signal_initiate_scan_of_playlist.connect(self.model.start_extract_of_songs_from_playlist_thread)
        self.view.signal_save_playlist.connect(self.model.start_saving_playlist_thread)
        self.view.signal_delete_playlist.connect(self.model.start_delete_selected_playlist_thread)

        # model signals that connect to the view slots
        self.model.signal_analysis_of_music_folder.connect(self.view.update_screen_information)
        self.model.signal_analysis_of_playlist.connect(self.view.update_playlist_table)
        self.model.signal_update_progress.connect(self.view.update_progress_bar)
        self.model.signal_error_message.connect(self.view.messagebox_system_error_detected)
        self.model.signal_playlist_successfully_saved.connect(self.view.reset_interface_after_saving_playlist)
        self.model.signal_playlist_successfully_deleted.connect(self.view.reset_interface_after_deleting_playlist)

        self.model.build_app_directory_and_setup_logger()

        self.show()

    # *** Main Window Methods ***
    def open_preferences_window(self) -> None:
        """
        Launches the preferences window.

        :return:
        """
        preferences_settings_data = self.model.preferences_data
        application_preferences_window = ApplicationPreferencesWindow(preferences_settings_data)
        application_preferences_window.signal_save_new_preferences_settings.connect(
            self.model.save_new_app_preferences_to_json_file
        )
        application_preferences_window.signal_clear_log_file.connect(self.model.remove_then_make_new_log_file)
        application_preferences_window.exec()

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