import logging
from PySide6 import QtCore as qtc
from .functions import (
    build_app_directory,
    setup_app_logger,
    setup_app_settings_file,
    load_app_settings,
    save_app_settings,
    delete_then_recreate_log_file,
)
from .threads import (
    ScanMusicFolderThread,
    SavingPlaylistThread,
    ExtractSongsFromPlaylistThread,
    DeletePlaylistThread
)

class Model(qtc.QObject):
    """The back-end of the application."""

    thread_pool = qtc.QThreadPool().globalInstance()

    # Signals that connect to view slots
    signal_error_message = qtc.Signal(object)
    signal_update_progress = qtc.Signal(int)
    signal_analysis_of_music_folder = qtc.Signal(list)
    signal_analysis_of_playlist = qtc.Signal(tuple)
    signal_playlist_successfully_saved = qtc.Signal()
    signal_playlist_successfully_deleted = qtc.Signal()

    def __init__(self):
        super().__init__()
        self.__app_settings_data = {}

# *** Methods that access Model or application files ***
    @property
    def preferences_data(self):
        return self.__app_settings_data.get("preferences")

    def build_app_directory_and_setup_logger(self) -> None:
        """
        Builds the app directory and sets up the logger for the application.

        :return:
        """
        build_app_directory()
        setup_app_settings_file()
        self.__app_settings_data = load_app_settings()

        logging_level_from_settings_file = (
            self.__app_settings_data.get("preferences")
            .get("logging_settings")
            .get("level")
        )
        setup_app_logger(logging_level_from_settings_file)

# *** Methods that don't use threads to complete a task ***
    @qtc.Slot(dict)
    def save_new_app_preferences_to_json_file(self, new_pref_settings: dict) -> None:
        """
        Saves the new preferences to a json file that is located in the application directory.

        :param new_pref_settings: The new preferences settings to save.
        :return:
        """
        logging.info("saving new preferences to json file")
        self.__app_settings_data["preferences"] = new_pref_settings
        save_app_settings(self.__app_settings_data)

    @qtc.Slot()
    def remove_then_make_new_log_file(self) -> None:
        """
        Removes the existing log file, and then recreates them.

        :return:
        """
        delete_then_recreate_log_file()

# *** Methods that use threads to complete a task ***
    @qtc.Slot(str)
    def start_scan_of_music_folder_thread(self, directory: str) -> None:
        """
        Starts the thread for scanning the Walkman Music Folder.

        :param directory: Location of the Walkman Music Folder.
        :return:
        """
        scan_music_folder_thread = ScanMusicFolderThread(directory)
        scan_music_folder_thread.signals.progress.connect(self.signal_update_progress)
        scan_music_folder_thread.signals.error.connect(self.signal_error_message)
        scan_music_folder_thread.signals.finished.connect(self.signal_analysis_of_music_folder)
        self.thread_pool.start(scan_music_folder_thread)

    @qtc.Slot(str)
    def start_extract_of_songs_from_playlist_thread(self, playlist_name: str, playlist_path: str) -> None:
        """
        Starts the thread for extracting songs from selected playlist.

        :param playlist_name: Name of the playlist.
        :param playlist_path: Path to the playlist.
        :return:
        """
        extract_songs_from_playlist_thread = ExtractSongsFromPlaylistThread(playlist_name, playlist_path)
        extract_songs_from_playlist_thread.signals.progress.connect(self.signal_update_progress)
        extract_songs_from_playlist_thread.signals.error.connect(self.signal_error_message)
        extract_songs_from_playlist_thread.signals.finished.connect(self.signal_analysis_of_playlist)
        self.thread_pool.start(extract_songs_from_playlist_thread)

    @qtc.Slot(tuple)
    def start_saving_playlist_thread(self, playlist_info: tuple) -> None:
        """
        Starts the thread for saving a new/existing playlist.

        :param playlist_info: A tuple containing the: songs that will go in playlist, playlist name,
        and directory to save the playlist in.
        :return:
        """
        save_playlist_thread = SavingPlaylistThread(*playlist_info)
        save_playlist_thread.signals.progress.connect(self.signal_update_progress)
        save_playlist_thread.signals.error.connect(self.signal_error_message)
        save_playlist_thread.signals.finished.connect(self.signal_playlist_successfully_saved)
        self.thread_pool.start(save_playlist_thread)

    @qtc.Slot(tuple)
    def start_delete_selected_playlist_thread(self, playlist_info: tuple) -> None:
        """
        Starts the thread for deleting selected playlist.

        :param playlist_info: A tuple containing the name of the playlist and where its directory location.
        :return:
        """
        delete_playlist_thread = DeletePlaylistThread(*playlist_info)
        delete_playlist_thread.signals.progress.connect(self.signal_update_progress)
        delete_playlist_thread.signals.error.connect(self.signal_error_message)
        delete_playlist_thread.signals.finished.connect(self.signal_playlist_successfully_deleted)
        self.thread_pool.start(delete_playlist_thread)
