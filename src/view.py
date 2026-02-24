from PySide6 import (
    QtWidgets as qtw,
    QtCore as qtc,
)
from .classes import ErrorEnum
from .custom_objects import (
    PlaylistTable,
    PlaylistTableView,
    MusicFolderTreeView,
    ModifiedQComboBox
)

class View(qtw.QWidget):
    """The front-end of the program"""

    # Signals that connect to model slots
    signal_initiate_scan_of_music_folder = qtc.Signal(str)
    signal_initiate_scan_of_playlist = qtc.Signal(str, str)
    signal_save_playlist = qtc.Signal(tuple)
    signal_delete_playlist = qtc.Signal(tuple)

    def __init__(self):
        super().__init__()

        self.playlist_has_been_modified = False # Keeps track when the playlist have been modified--add/remove song(s)

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
        self.cb_playlist_selection = ModifiedQComboBox(
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
        self.table_songs_in_playlist_view.signal_remove_song.connect(self.song_to_remove_from_playlist)

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
        self.music_folder_tree_view.signal_song_to_add.connect(self.add_song_to_playlist)

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
        self.btn_undo_changes_button = qtw.QPushButton("Undo Changes", self)
        self.btn_undo_changes_button.clicked.connect(self.undo_changes_to_playlist)
        self.btn_undo_changes_button.setEnabled(False)
        self.progress_bar = qtw.QProgressBar(self)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)

        layout_buttons_and_progress = qtw.QHBoxLayout()
        layout_buttons_and_progress.addWidget(self.btn_save_button)
        layout_buttons_and_progress.addWidget(self.btn_delete_button)
        layout_buttons_and_progress.addWidget(self.btn_undo_changes_button)
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
        if self.le_playlist_name.text() != "":
            self._disable_all_widgets()

            self.signal_save_playlist.emit((
                self.table_songs_in_playlist_model.extract_data(),
                self.le_playlist_name.text(),
                self.le_walkman_music_folder.text(),
            ))

        else:
            qtw.QMessageBox.information(
                self,
                'Name for Playlist',
                'Please provide a name for the paylist to save the playlist.',
            )

    @qtc.Slot()
    def delete_playlist(self):
        """
        Deletes the playlist from Walkman MUSIC folder.

        :return:
        """
        response = qtw.QMessageBox.question(
            self,
            "Delete Playlist?",
            "Are you sure you want to delete the playlist?",
            buttons=qtw.QMessageBox.StandardButton.Yes | qtw.QMessageBox.StandardButton.No,
            defaultButton=qtw.QMessageBox.StandardButton.Yes
        )

        if response == qtw.QMessageBox.StandardButton.Yes:
            self._disable_all_widgets()

            self.signal_delete_playlist.emit((self.le_playlist_name.text(), self.le_walkman_music_folder.text()))

    @qtc.Slot()
    def undo_changes_to_playlist(self):
        """
        Undo all changes to playlist.

        :return:
        """
        response = qtw.QMessageBox.warning(
            self,
            "Undo Changes?",
            "Are you sure you wish to undo all changes to playlist?",
            buttons=qtw.QMessageBox.StandardButton.Yes | qtw.QMessageBox.StandardButton.No,
            defaultButton=qtw.QMessageBox.StandardButton.Yes
        )

        if response == qtw.QMessageBox.StandardButton.Yes:
            self.table_songs_in_playlist_model.clear()

            self._disable_all_widgets()

            if self.cb_playlist_selection.currentIndex() > 1:
                self.signal_initiate_scan_of_playlist.emit(self.cb_playlist_selection.currentText(), self.le_walkman_music_folder.text())

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
            self.le_walkman_music_folder.setEnabled(False)
            self.btn_select_walkman_music_folder.setEnabled(False)

            # clear out old information
            self.cb_playlist_selection.clear()
            self.cb_playlist_selection.addItems(['---', 'New Playlist'])
            self.table_songs_in_playlist_model.clear()

            self.le_walkman_music_folder.setText(directory)
            self.signal_initiate_scan_of_music_folder.emit(directory)

    @qtc.Slot()
    def user_pasted_in_directory(self) -> None:
        """
        Runs when the user pastes in the directory they wish to scan and hits enter.

        :return:
        """
        self.le_walkman_music_folder.setEnabled(False)
        self.btn_select_walkman_music_folder.setEnabled(False)

        # clear out old information
        self.cb_playlist_selection.clear()
        self.cb_playlist_selection.addItems(['---', 'New Playlist'])
        self.table_songs_in_playlist_model.clear()

        self.signal_initiate_scan_of_music_folder.emit(self.le_walkman_music_folder.text())

    @qtc.Slot()
    def playlist_selection_changed(self, combo_index: int) -> None:
        """
        Runs when the user selects a different option from the playlist combo-box.

        :param combo_index: The index of the combo-box.
        :return:
        """
        if combo_index == 0:
            self.le_playlist_name.setEnabled(False)
            self.table_songs_in_playlist_view.setEnabled(False)
            self.music_folder_tree_view.setEnabled(False)
        elif combo_index >= 1:
            self.table_songs_in_playlist_view.setEnabled(True)
            self.music_folder_tree_view.setEnabled(True)
            self.btn_save_button.setEnabled(False)
            self.btn_undo_changes_button.setEnabled(False)

            if not self.table_songs_in_playlist_model.is_table_empty():
                self.table_songs_in_playlist_model.clear()

            if combo_index == 1:
                self.le_playlist_name.setEnabled(True)
                self.btn_delete_button.setEnabled(False)
                self.le_playlist_name.clear()
            else:
                self.le_playlist_name.setEnabled(False)
                self.btn_delete_button.setEnabled(True)
                self.le_playlist_name.setText(self.cb_playlist_selection.currentText())
                self.signal_initiate_scan_of_playlist.emit(self.cb_playlist_selection.currentText(), self.le_walkman_music_folder.text())

    @qtc.Slot(list)
    def update_screen_information(self, list_of_playlists):
        """
        Loads in the playlist(s) found in the Walkman MUSIC folder, and generates the folder
        structure for the music folder tree view.

        :param list_of_playlists: A list of playlist(s) found in the Walkman MUSIC folder.
        :return:
        """

        # add in new information
        self.cb_playlist_selection.addItems(list_of_playlists)
        self.music_folder_tree_view.set_root_path(
            self.le_walkman_music_folder.text(),
            ["*.mp3", "*.wav", "*.m4a", "*.flac"],
            [1,3],
        )

        self.le_walkman_music_folder.setEnabled(True)
        self.btn_select_walkman_music_folder.setEnabled(True)
        self.cb_playlist_selection.setEnabled(True)
        self.le_playlist_name.setEnabled(True)

        self.progress_bar.reset()

    @qtc.Slot(int)
    def update_progress_bar(self, progress_value: int) -> None:
        """
        Updates the screen progress bar.

        :param progress_value: The value to set the progress bar to.
        :return:
        """
        self.progress_bar.setValue(progress_value)

    @qtc.Slot()
    def reset_interface_after_deleting_playlist(self) -> None:
        """
        Resets the interface after the deleting playlist.

        :return:
        """
        self.table_songs_in_playlist_model.clear()
        self.cb_playlist_selection.remove_item(self.le_playlist_name.text())
        self.le_playlist_name.clear()

        self.le_walkman_music_folder.setEnabled(True)
        self.btn_select_walkman_music_folder.setEnabled(True)
        self.cb_playlist_selection.setEnabled(True)

        self.progress_bar.reset()

    @qtc.Slot()
    def reset_interface_after_saving_playlist(self) -> None:
        """
        Resets the interface after the saving playlist.

        :return:
        """
        self.progress_bar.reset()
        self.table_songs_in_playlist_model.clear()
        self.le_walkman_music_folder.setEnabled(True)
        self.btn_select_walkman_music_folder.setEnabled(True)
        self.cb_playlist_selection.setEnabled(True)

        # Append playlist to the list of existing playlists if it does not exist in it
        if self.le_playlist_name.text() not in self.cb_playlist_selection.all_items():
            self.cb_playlist_selection.addItem(self.le_playlist_name.text())

        self.le_playlist_name.clear()
        self.cb_playlist_selection.setCurrentIndex(0)

# *** Method(s) that affect Playlist table ***
    @qtc.Slot(tuple)
    def add_song_to_playlist(self, song: tuple) -> None:
        """
        Adds a song to the playlist.

        :param song: The song to be added to the playlist.
        :return:
        """
        self.table_songs_in_playlist_model.insert_row(
            position=self.table_songs_in_playlist_model.rowCount(),
            row=1,
            data=song
        )
        self.btn_save_button.setEnabled(True)
        self.btn_undo_changes_button.setEnabled(True)
        self.playlist_has_been_modified = True

    @qtc.Slot(int)
    def song_to_remove_from_playlist(self, song_index: int) -> None:
        """
        Removes a song from the playlist.

        :param song_index: The index of the song to be removed from the playlist.
        :return:
        """
        self.table_songs_in_playlist_model.removeRow(position=song_index)
        self.btn_save_button.setEnabled(True)
        self.btn_undo_changes_button.setEnabled(True)
        self.playlist_has_been_modified = True

    @qtc.Slot(tuple)
    def update_playlist_table(self, songs_list: tuple) -> None:
        """
        Updates the playlist table with the given songs list.

        :param songs_list: The songs list to be updated.
        """
        self.progress_bar.reset()
        self.table_songs_in_playlist_model.insert_rows(
            position=self.table_songs_in_playlist_model.rowCount(),
            rows=len(songs_list),
            data=reversed(songs_list) # reversing the order so it matches the order in the playlist
        )

        self.le_walkman_music_folder.setEnabled(True)
        self.btn_select_walkman_music_folder.setEnabled(True)
        self.cb_playlist_selection.setEnabled(True)
        self.table_songs_in_playlist_view.setEnabled(True)
        self.music_folder_tree_view.setEnabled(True)

        if self.cb_playlist_selection.currentIndex() == 1:
            self.le_playlist_name.setEnabled(True)
        elif self.cb_playlist_selection.currentIndex() >= 2:
            self.btn_delete_button.setEnabled(True)

        self.playlist_has_been_modified = False

# *** Method(s) that launch a messagebox ***
    @qtc.Slot(object)
    def messagebox_system_error_detected(self, error: ErrorEnum) -> None:
        """
        Launches the messagebox to inform the user a system error had occurred.

        :return:
        """
        message = ''
        match error:
            case ErrorEnum.SCAN_FOLDER_ERROR:
                message = 'An error occurred while scanning the folder.'
            case ErrorEnum.SAVE_PLAYLIST_ERROR:
                message = 'An error occurred while saving the playlist.'
            case ErrorEnum.EXTRACT_SONGS_ERROR:
                message = 'An error occurred while extracting the songs from the playlist.'
            case ErrorEnum.DELETE_PLAYLIST_ERROR:
                message = 'An error occurred while deleting the playlist.'

        response = qtw.QMessageBox.critical(
            self,
            'System Error',
            message
        )

        if response == qtw.QMessageBox.StandardButton.Ok:
            self.progress_bar.reset()

            # Enable the correct widgets based on error raised
            match error:
                case ErrorEnum.SCAN_FOLDER_ERROR:
                    self.le_walkman_music_folder.setEnabled(True)
                    self.btn_select_walkman_music_folder.setEnabled(True)

                case ErrorEnum.SAVE_PLAYLIST_ERROR:
                    self.le_walkman_music_folder.setEnabled(True)
                    self.btn_select_walkman_music_folder.setEnabled(True)
                    self.cb_playlist_selection.setEnabled(True)
                    self.table_songs_in_playlist_view.setEnabled(True)
                    self.music_folder_tree_view.setEnabled(True)
                    self.btn_save_button.setEnabled(True)
                    self.btn_undo_changes_button.setEnabled(True)

                    if self.cb_playlist_selection.currentIndex() == 1:
                        self.le_playlist_name.setEnabled(True)
                    elif self.cb_playlist_selection.currentIndex() >= 2:
                        self.btn_delete_button.setEnabled(True)

                case ErrorEnum.EXTRACT_SONGS_ERROR:
                    self.cb_playlist_selection.setEnabled(True)
                    self.le_playlist_name.clear()
                    self.cb_playlist_selection.setCurrentIndex(0)

                case ErrorEnum.DELETE_PLAYLIST_ERROR:
                    self.le_walkman_music_folder.setEnabled(True)
                    self.btn_select_walkman_music_folder.setEnabled(True)
                    self.cb_playlist_selection.setEnabled(True)
                    self.table_songs_in_playlist_view.setEnabled(True)
                    self.music_folder_tree_view.setEnabled(True)
                    self.btn_delete_button.setEnabled(True)

                    if self.playlist_has_been_modified:
                        self.btn_save_button.setEnabled(True)
                        self.btn_undo_changes_button.setEnabled(True)

# *** Method(s) that are private
    def _disable_all_widgets(self) -> None:
        self.le_walkman_music_folder.setEnabled(False)
        self.btn_select_walkman_music_folder.setEnabled(False)
        self.cb_playlist_selection.setEnabled(False)
        self.le_playlist_name.setEnabled(False)
        self.table_songs_in_playlist_view.setEnabled(False)
        self.music_folder_tree_view.setEnabled(False)
        self.btn_save_button.setEnabled(False)
        self.btn_delete_button.setEnabled(False)
        self.btn_undo_changes_button.setEnabled(False)