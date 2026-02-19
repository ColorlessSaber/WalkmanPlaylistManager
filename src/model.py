import pathlib

from PySide6 import QtCore as qtc
from .threads import (
    ScanMusicFolderThread,
    SavingPlaylistThread,
    ExtractSongsFromPlaylistThread
)

from .classes import ErrorEnum

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

# *** Methods that don't use threads to complete a task ***
    @qtc.Slot(tuple)
    def delete_selected_playlist(self, playlist_info: tuple) -> None:
        """
        Deletes the selected playlist.

        :param playlist_info: A tuple containing the name of the playlist and where its directory location.
        :return:
        """
        try: # TODO make this a thread
            playlist_name, directory = playlist_info
            file_path = pathlib.Path(directory).joinpath(playlist_name + '.M3U8')
            file_path.unlink()
        except FileNotFoundError:
            self.signal_error_message.emit(ErrorEnum.DELETE_PLAYLIST_ERROR)
        else:
            self.signal_playlist_successfully_deleted.emit()

# *** Methods that use threads to complete a task ***
    @qtc.Slot(str)
    def start_scan_of_music_folder_thread(self, directory: str) -> None:
        """
        Starts the thread for scanning the Walkman Music Folder.

        :param directory: Location of the Walkman Music Folder.
        :return:
        """
        scan_music_folder_thread = ScanMusicFolderThread(directory)
        scan_music_folder_thread.signals.progress.connect(self.signal_update_progress.emit)
        scan_music_folder_thread.signals.error.connect(self.signal_error_message.emit)
        scan_music_folder_thread.signals.finished.connect(self.signal_analysis_of_music_folder.emit)
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
        extract_songs_from_playlist_thread.signals.progress.connect(self.signal_update_progress.emit)
        extract_songs_from_playlist_thread.signals.error.connect(self.signal_error_message.emit)
        extract_songs_from_playlist_thread.signals.finished.connect(self.signal_analysis_of_playlist.emit)
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
        save_playlist_thread.signals.progress.connect(self.signal_update_progress.emit)
        save_playlist_thread.signals.error.connect(self.signal_error_message.emit)
        save_playlist_thread.signals.finished.connect(self.signal_playlist_successfully_saved.emit)
        self.thread_pool.start(save_playlist_thread)