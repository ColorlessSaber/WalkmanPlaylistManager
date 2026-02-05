from typing import Any
from PySide6 import (
    QtWidgets as qtw,
    QtCore as qtc,
)
from .pyside_table_object import GenericTable

class PlaylistTable(GenericTable):
    """Table for showing what song(s) are in the playlist"""
    def insert_file(self, position, rows, row_data, parent=qtc.QModelIndex()) -> None:
        """Insert a new row into the table"""
        self.beginInsertRows(parent, position, position + rows - 1)
        for _ in range(rows):
            self._data.insert(position, row_data)
        self.endInsertRows()

    def remove_file(self, position, rows, parent=qtc.QModelIndex()) -> None:
        """Remove a single row from the table"""
        self.beginRemoveRows(parent, position, position + rows - 1)
        for _ in range(rows):
            del(self._data[position])
        self.endRemoveRows()

    def extract_data(self) -> list[Any]:
        """
        Returns the data that is stored in the table
        """
        return self._data

class MusicFolderTable(GenericTable):
    """Table for showing what folders/song files are in the folder"""

class View(qtw.QWidget):
    """The front-end of the program"""

    signal_initiate_scan_of_music_folder = qtc.Signal(str)

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
        self.cb_playlist_selection.addItem('New Playlist', 'new_playlist')
        self.cb_playlist_selection.currentIndexChanged.connect(self.playlist_selection_changed)
        lbl_playlist_name = qtw.QLabel("Playlist Name:", self)
        self.le_playlist_name = qtw.QLineEdit(self)

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
        self.table_songs_in_playlist_view = qtw.QTableView(self)
        self.table_songs_in_playlist_view.setSortingEnabled(False)
        self.table_songs_in_playlist_model = PlaylistTable(
            read_only_columns=[0],
            column_names=['Song'],
        )
        self.table_songs_in_playlist_view.setModel(self.table_songs_in_playlist_model)

        layout_songs_in_playlist = qtw.QVBoxLayout()
        layout_songs_in_playlist.addWidget(lbl_songs_in_playlist)
        layout_songs_in_playlist.addWidget(self.table_songs_in_playlist_view)

        # Music folder view section
        lbl_music_folder = qtw.QLabel("Music Folder:", self)
        self.table_music_folder_view = qtw.QTableView(self)
        self.table_music_folder_view.setSortingEnabled(False)
        self.table_music_folder_model = MusicFolderTable(
            read_only_columns=[0],
            column_names=['']
        )
        self.table_music_folder_view.setModel(self.table_music_folder_model)

        layout_music_folder = qtw.QVBoxLayout()
        layout_music_folder.addWidget(lbl_music_folder)
        layout_music_folder.addWidget(self.table_music_folder_view)

        # Buttons and progress bar section
        self.btn_save_button = qtw.QPushButton("Save", self)
        self.btn_save_button.clicked.connect(self.save_playlist)
        self.btn_delete_button = qtw.QPushButton("Delete", self)
        self.btn_delete_button.clicked.connect(self.delete_playlist)
        self.btn_cancel_button = qtw.QPushButton("Cancel", self)
        self.btn_cancel_button.clicked.connect(self.cancel)
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
        Runs when the user selects a different option from the combo-box.

        :param combo_index: The index of the combo-box.
        :return:
        """
        print(f"{combo_index} selected")

    @qtc.Slot(object)
    def update_screen_information(self, music_folder_info):
        """
        Takes the given music_folder_info, unloads the information stored inside it and
        update the screen information.

        :param music_folder_info: An object that holds information about the Walkman MUSIC folder.
        :return:
        """
        print(music_folder_info)

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
            self.reset_progress_bar()