from PySide6 import QtCore as qtc
from .threads import ScanMusicFolderThread

class Model(qtc.QObject):
    """The back-end of the application."""

    thread_pool = qtc.QThreadPool()

    # Signals that connect to view slots
    signal_error_message = qtc.Signal()
    signal_update_progress = qtc.Signal(int)
    signal_analysis_of_music_folder = qtc.Signal(object)

# *** Methods that don't use threads to complete a task ***

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