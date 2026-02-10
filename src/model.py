import re
from PySide6 import QtCore as qtc
from .threads import ScanMusicFolderThread

class Model(qtc.QObject):
    """The back-end of the application."""

    thread_pool = qtc.QThreadPool()

    # Signals that connect to view slots
    signal_error_message = qtc.Signal()
    signal_update_progress = qtc.Signal(int)
    signal_analysis_of_music_folder = qtc.Signal(object)
    signal_analysis_of_playlist = qtc.Signal(list)

# *** Methods that don't use threads to complete a task ***
    @qtc.Slot(str)
    def read_in_playlist(self, playlist_path: str) -> None:
        """
        Opens the playlist, reads the songs in the playlist, save them to a list and send it to back.

        :param playlist_path: Path to the playlist.
        :return:
        """
        playlist_markers = re.compile(r"^#EXT\w+") # markers used in Walkman playlists
        with open(playlist_path, "r") as file:
            clean_list_of_songs = [line_item.strip() for line_item in file.readlines()
                                   if not playlist_markers.match(line_item)]
        # TODO separate artist, album, and song per entry in clean_list_of_songs.
        self.signal_analysis_of_playlist.emit(clean_list_of_songs)

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
