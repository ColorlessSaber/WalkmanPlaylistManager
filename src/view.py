import pathlib
from typing import Any
from PySide6 import (
    QtWidgets as qtw,
    QtCore as qtc,
)
from custom_objects import GenericTable, GenericTableView, GenericFileSystemTreeView

class PlaylistTable(GenericTable):
    """Table for showing what song(s) are in the playlist"""
    def insert_rows(self, position, rows, data, parent=qtc.QModelIndex()) -> None:
        """Insert rows into the table"""
        self.beginInsertRows(parent, position, position + rows - 1)
        for item in data:
            self._data.insert(position, item)
        self.endInsertRows()

    def extract_data(self) -> list[Any]:
        """
        Returns the data that is stored in the table
        """
        return self._data

    def is_table_empty(self) -> bool:
        """
        Returns True if the table is empty.
        """
        return True if not self._data else False

class PlaylistTableView(GenericTableView):
    """
    The playlist table view
    """
    signal_remove_song = qtc.Signal(int)

    def context_menu(self, pos: qtc.QPoint) -> None:
        menu = qtw.QMenu()
        remove_song_action = menu.addAction("Remove Song")

        action = menu.exec_(self.mapToGlobal(pos))
        if action == remove_song_action:
            self.signal_remove_song.emit(self.indexAt(pos).row())

class MusicFolderTreeView(GenericFileSystemTreeView):
    """
    The music folder tree view
    """

class View(qtw.QWidget):
    """The front-end of the program"""

    # Signals that connect to model slots
    signal_initiate_scan_of_music_folder = qtc.Signal(str)
    signal_initiate_scan_of_playlist = qtc.Signal(str)

    def __init__(self):
        super().__init__()

        # Walkman MUSIC folder selection section
        lbl_walkman_music_folder = qtw.QLabel("Walkman Music Folder:", self)
        self.le_walkman_music_folder = qtw.QLineEdit(self)
        self.le_walkman_music_folder.returnPressed.connect(self.user_pasted_in_directory)
        self.btn_select_walkman_music_folder = qtw.QPushButton("Select Folder", self)
        self.btn_select_walkman_music_folder.clicked.connect(self.select_walkman_music_folder)
        layout_walkman_music_folder = qtw.QHBoxLayout()
        layout_walkman_music_folder.addWidget(lbl_walkman_music_folder)
        layout_walkman_music_folder.addWidget(self.le_walkman_music_folder)
        layout_walkman_music_folder.addWidget(self.btn_select_walkman_music_folder)

        # Playlist selection/creation section
        self.cb_playlist_selection = qtw.QComboBox(
            self,
            editable=False,
            insertPolicy=qtw.QComboBox.InsertPolicy.InsertAtBottom
        )
        self.cb_playlist_selection.addItems(['---', 'New Playlist'])
        self.cb_playlist_selection.currentIndexChanged.connect(self.playlist_selection_changed)
        self.cb_playlist_selection.setEnabled(False)
        lbl_playlist_name = qtw.QLabel("Playlist Name:", self)
        self.le_playlist_name = qtw.QLineEdit(self)
        self.le_playlist_name.setEnabled(False)

        self.playlist_section_group = qtw.QGroupBox("Playlist Selection/Creation", self)
        self.playlist_section_group.setObjectName("playlist_selection_group")
        self.playlist_section_group.setLayout(qtw.QHBoxLayout())
        self.playlist_section_group.layout().addWidget(self.cb_playlist_selection)
        self.playlist_section_group.layout().addWidget(lbl_playlist_name)
        self.playlist_section_group.layout().addWidget(self.le_playlist_name)
        self.playlist_section_group.setStyleSheet("""
            #playlist_selection_group {
                border: 2px solid grey;
                border-radius: 5px;
                padding-top: 16px;
                font-weight: bold;
            }
        """)

        # Songs in playlist view section
        lbl_songs_in_playlist = qtw.QLabel("Songs in Playlist", self)
        lbl_songs_in_playlist.setStyleSheet("""
            QLabel {
                font-size: 14px;
                text-decoration: underline;
            }   
        """)
        self.table_songs_in_playlist_view = PlaylistTableView(self)
        self.table_songs_in_playlist_view.setSortingEnabled(False)
        self.table_songs_in_playlist_model = PlaylistTable(
            read_only_columns=[0],
            column_names=['Artist', 'Album', 'Song'],
        )
        self.table_songs_in_playlist_view.setModel(self.table_songs_in_playlist_model)
        self.table_songs_in_playlist_view.setEnabled(False)
        self.table_songs_in_playlist_view.signal_remove_song.connect(self.table_songs_in_playlist_model.removeRow)

        layout_songs_in_playlist = qtw.QVBoxLayout()
        layout_songs_in_playlist.addWidget(lbl_songs_in_playlist)
        layout_songs_in_playlist.addWidget(self.table_songs_in_playlist_view)

        # Music folder view section
        lbl_music_folder = qtw.QLabel("Music Folder", self)
        lbl_music_folder.setStyleSheet("""
            QLabel {
                font-size: 14px;
                text-decoration: underline;
            }   
        """)
        self.music_folder_tree_view = MusicFolderTreeView(self)
        self.music_folder_tree_view.setEnabled(False)

        layout_music_folder = qtw.QVBoxLayout()
        layout_music_folder.addWidget(lbl_music_folder)
        layout_music_folder.addWidget(self.music_folder_tree_view)

        # Buttons and progress bar section
        self.btn_save_button = qtw.QPushButton("Save", self)
        self.btn_save_button.clicked.connect(self.save_playlist)
        self.btn_save_button.setEnabled(False)
        self.btn_delete_button = qtw.QPushButton("Delete", self)
        self.btn_delete_button.clicked.connect(self.delete_playlist)
        self.btn_delete_button.setEnabled(False)
        self.btn_cancel_button = qtw.QPushButton("Cancel", self)
        self.btn_cancel_button.clicked.connect(self.cancel)
        self.btn_cancel_button.setEnabled(False)
        self.progress_bar = qtw.QProgressBar(self)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)

        layout_buttons_and_progress = qtw.QHBoxLayout()
        layout_buttons_and_progress.addWidget(self.btn_save_button)
        layout_buttons_and_progress.addWidget(self.btn_delete_button)
        layout_buttons_and_progress.addWidget(self.btn_cancel_button)
        layout_buttons_and_progress.addWidget(self.progress_bar)

        # Combining all layouts and widgets
        layout_playlist_and_music_folder_tables = qtw.QHBoxLayout()
        layout_playlist_and_music_folder_tables.addLayout(layout_songs_in_playlist)
        layout_playlist_and_music_folder_tables.addLayout(layout_music_folder)

        main_layout = qtw.QVBoxLayout()
        main_layout.addLayout(layout_walkman_music_folder)
        main_layout.addWidget(self.playlist_section_group)
        main_layout.addLayout(layout_playlist_and_music_folder_tables)
        main_layout.addLayout(layout_buttons_and_progress)

        self.setLayout(main_layout)

    @qtc.Slot()
    def save_playlist(self):
        """
        Saves the playlist to the Walkman MUSIC folder.

        :return:
        """
        print("Saving Playlist")

    @qtc.Slot()
    def delete_playlist(self):
        """
        Deletes the playlist from Walkman MUSIC folder.

        :return:
        """
        print("Deleting Playlist")

    @qtc.Slot()
    def cancel(self):
        """
        Cancels all changes made to the playlist.

        :return:
        """
        print("Canceling changes to playlist")

    @qtc.Slot()
    def select_walkman_music_folder(self) -> None:
        """
        Opens a file dialog window to allow user to select their Walkman MUSIC folder.

        :return:
        """
        directory = qtw.QFileDialog.getExistingDirectory(
            self,
            'Select folder...',
            qtc.QDir.homePath()
        )

        if directory:
            self._enable_widgets(False)
            self.le_walkman_music_folder.setText(directory)
            self.signal_initiate_scan_of_music_folder.emit(directory)

    @qtc.Slot()
    def user_pasted_in_directory(self) -> None:
        """
        Runs when the user pastes in the directory they wish to scan and hits enter.

        :return:
        """
        self.signal_initiate_scan_of_music_folder.emit(self.le_walkman_music_folder.text())

    @qtc.Slot()
    def playlist_selection_changed(self, combo_index: int) -> None:
        """
        Runs when the user selects a different option from the playlist combo-box.

        :param combo_index: The index of the combo-box.
        :return:
        """
        print("combo-index:", combo_index)
        if combo_index == 0:
            self.le_playlist_name.setEnabled(False)
            self.table_songs_in_playlist_view.setEnabled(False)
            self.music_folder_tree_view.setEnabled(False)
        elif combo_index >= 1:
            self.table_songs_in_playlist_view.setEnabled(True)
            self.music_folder_tree_view.setEnabled(True)

            if not self.table_songs_in_playlist_model.is_table_empty():
                self.table_songs_in_playlist_model.clear()

            if combo_index == 1:
                self.le_playlist_name.setEnabled(True)
                self.le_playlist_name.clear()
            else:
                self.le_playlist_name.setEnabled(False)
                self.le_playlist_name.setText(self.cb_playlist_selection.currentText().replace(".M3U8", ""))
                music_folder_path = pathlib.Path(self.le_walkman_music_folder.text()).joinpath(self.cb_playlist_selection.currentText())
                self.signal_initiate_scan_of_playlist.emit(str(music_folder_path))

    @qtc.Slot(list)
    def update_screen_information(self, list_of_playlists):
        """
        Loads in the playlist(s) found in the Walkman MUSIC folder, and generates the folder
        structure for the music folder tree view.

        :param list_of_playlists: A list of playlist(s) found in the Walkman MUSIC folder.
        :return:
        """
        # clear out old information
        self.cb_playlist_selection.clear()
        self.cb_playlist_selection.addItems(['---', 'New Playlist'])
        self.table_songs_in_playlist_model.clear()

        # add in new information
        self.cb_playlist_selection.addItems(list_of_playlists)
        self.music_folder_tree_view.set_root_path(
            self.le_walkman_music_folder.text(),
            ["*.mp3", "*.wav", "*.m4a", "*.flac"],
            [1,3],
        )

        self._enable_widgets(True)
        self.progress_bar.reset()

    @qtc.Slot(list)
    def update_playlist_table(self, songs_list: list) -> None:
        """
        Updates the playlist table with the given songs list.

        :param songs_list: The songs list to be updated.
        """
        self.table_songs_in_playlist_model.insert_rows(
            position=self.table_songs_in_playlist_model.rowCount(),
            rows=len(songs_list),
            data=songs_list
        )
        self.table_songs_in_playlist_view.resizeColumnsToContents()

    @qtc.Slot(int)
    def update_progress_bar(self, progress_value: int) -> None:
        """
        Updates the screen progress bar.

        :param progress_value: The value to set the progress bar to.
        :return:
        """
        self.progress_bar.setValue(progress_value)

    @qtc.Slot()
    def reset_progress_bar(self) -> None:
        """
        Resets the screen progress bar.

        :return:
        """
        self.progress_bar.reset()

# *** Music folder table commands ***

# *** Playlist table commands ***

# *** Method(s) that launch a messagebox ***

    @qtc.Slot()
    def messagebox_system_error_detected(self) -> None:
        """
        Launches the messagebox to inform the user a system error had occurred.

        :return:
        """
        response = qtw.QMessageBox.critical(
            self,
            'System Error',
            'The program ran into an error while working a process.'
        )

        if response == qtw.QMessageBox.StandardButton.Ok:
            self.progress_bar.reset()
            self.le_walkman_music_folder.setEnabled(True)
            self.btn_select_walkman_music_folder.setEnabled(True)

# *** Method(s) that are private ***

    def _enable_widgets(self, enable: bool) -> None:
        """
        Enables / disables widgets depending on the value of `enable`.

        :param enable: Sets the enable / disable status of widget.
        :return:
        """
        self.le_walkman_music_folder.setEnabled(enable)
        self.btn_select_walkman_music_folder.setEnabled(enable)
        self.cb_playlist_selection.setEnabled(enable)
        self.btn_save_button.setEnabled(enable)
        self.btn_delete_button.setEnabled(enable)
        self.btn_cancel_button.setEnabled(enable)
