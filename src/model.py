from PySide6 import QtCore as qtc
from .threads import ScanMusicFolderThread
from .functions import find_songs_in_playlist

class Model(qtc.QObject):
    """The back-end of the application."""

    thread_pool = qtc.QThreadPool()

    # Signals that connect to view slots
    signal_error_message = qtc.Signal()
    signal_update_progress = qtc.Signal(int)
    signal_analysis_of_music_folder = qtc.Signal(list)
    signal_analysis_of_playlist = qtc.Signal(list)

# *** Methods that don't use threads to complete a task ***
    @qtc.Slot(str)
    def read_in_playlist(self, playlist_path: str) -> None:
        """
        Opens the playlist; reads the songs in the playlist; and save each song in a list where each entry is
        the song's artist, album, and name.

        :param playlist_path: Path to the playlist.
        :return:
        """
        songs_in_playlist = find_songs_in_playlist(playlist_path)
        self.signal_analysis_of_playlist.emit(songs_in_playlist)

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
