from typing import Any
from PySide6 import (
    QtWidgets as qtw,
    QtCore as qtc,
    QtGui as qtg,
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

    def __init__(self):
        super().__init__()

        # Walkman MUSIC folder selection section
        lbl_walkman_music_folder = qtw.QLabel("Walkman Music Folder:", self)
        self.le_walkman_music_folder = qtw.QLineEdit(self)
        self.btn_select_walkman_music_folder = qtw.QPushButton("Select Folder", self)
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
                front-weight: bold;
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
        self.btn_delete_button = qtw.QPushButton("Delete", self)
        self.btn_cancel_button = qtw.QPushButton("Cancel", self)
        self.progress_bar = qtw.QProgressBar(self)

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

