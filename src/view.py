from typing import Any
from PySide6 import (
    QtWidgets as qtw,
    QtCore as qtc,
)
from custom_objects import (
    GenericTable,
    GenericTableView,
    GenericFileSystemTreeView,
    ModifiedQComboBox,
)

class PlaylistTable(GenericTable):
    """Table for showing what song(s) are in the playlist"""
    def insert_rows(self, position, rows, data, parent=qtc.QModelIndex()) -> None:
        """Insert rows into the table"""
        self.beginInsertRows(parent, position, position + rows - 1)
        for item in data:
            self._data.insert(position, item)
        self.endInsertRows()

    def insert_row(self, position, row, data, parent=qtc.QModelIndex()) -> None:
        """Insert a single row into the table"""
        self.beginInsertRows(parent, position, position + row - 1)
        self._data.insert(position, data)
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

    signal_song_to_add = qtc.Signal(str)

    def context_menu(self, pos: qtc.QPoint) -> None:
        # confirm the selection from the model is valid and the model had
        # initialized properly
        selection_model = self._tree_view.selectionModel()
        if not selection_model or not selection_model.hasSelection():
            return

        # confirm the index is valid (IE, the user clicked on an item)
        index = selection_model.currentIndex()
        if not index.isValid():
            return

        menu = qtw.QMenu()
        add_song_to_playlist_action = menu.addAction("Add Song to Playlist")

        if self._model.fileInfo(index).isFile():
            action = menu.exec_(self.mapToGlobal(pos))
            song_file = self._model.filePath(index)

            if action == add_song_to_playlist_action:
                self.signal_song_to_add.emit(song_file)


class View(qtw.QWidget):
    """The front-end of the program"""

    # Signals that connect to model slots
    signal_initiate_scan_of_music_folder = qtc.Signal(str)
    signal_initiate_scan_of_playlist = qtc.Signal(str, str)
    signal_prep_song_for_playlist = qtc.Signal(str)
    signal_save_playlist = qtc.Signal(tuple)

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
        self.music_folder_tree_view.signal_song_to_add.connect(self.signal_prep_song_for_playlist)

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
            self.le_walkman_music_folder.setEnabled(False)
            self.btn_select_walkman_music_folder.setEnabled(False)
            self.cb_playlist_selection.setEnabled(False)
            self.le_playlist_name.setEnabled(False)
            self.table_songs_in_playlist_view.setEnabled(False)
            self.music_folder_tree_view.setEnabled(False)
            self.btn_save_button.setEnabled(False)
            self.btn_delete_button.setEnabled(False)
            self.btn_undo_changes_button.setEnabled(False)

            self.signal_save_playlist.emit((
                self.table_songs_in_playlist_model.extract_data(),
                self.le_playlist_name.text(),
                self.le_walkman_music_folder.text(),
            ))

        else:
            qtw.QMessageBox.information(
                self,
                'Name for Paylist',
                'Please provide a name for the paylist to save the playlist.',
            )

    @qtc.Slot()
    def delete_playlist(self):
        """
        Deletes the playlist from Walkman MUSIC folder.

        :return:
        """
        print("Deleting Playlist")

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
            self.btn_save_button.setEnabled(False)
            self.btn_undo_changes_button.setEnabled(False)

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
    def reset_progress_bar(self) -> None:
        """
        Resets the screen progress bar.

        :return:
        """
        self.progress_bar.reset()

# *** Method(s) that affect Music folder table ***
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

    @qtc.Slot(int)
    def song_to_remove_from_playlist(self, song_index: int) -> None:
        """
        Removes a song from the playlist.

        :param song_index: The index of the song to be removed from the playlist.
        :return:
        """
        self.table_songs_in_playlist_model.removeRow(row=song_index)
        self.btn_save_button.setEnabled(True)
        self.btn_undo_changes_button.setEnabled(True)

# *** Method(s) that affect Playlist table ***
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

# *** Method(s) that launch a messagebox ***

    @qtc.Slot()
    def messagebox_playlist_saved(self) -> None:
        """
        Launches messagebox informing the user the playlist was saved.

        :return:
        """
        response = qtw.QMessageBox.information(
            self,
            'Playlist Saved!',
            'The playlist was saved successfully!'
        )

        if response == qtw.QMessageBox.StandardButton.Ok:
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
        #TODO add in logic or something to know of the state of the interface when error occurred to enable correct widgets
        if response == qtw.QMessageBox.StandardButton.Ok:
            self.progress_bar.reset()
            self.le_walkman_music_folder.setEnabled(True)
            self.btn_select_walkman_music_folder.setEnabled(True)
