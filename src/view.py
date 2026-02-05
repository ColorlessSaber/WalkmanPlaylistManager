from PySide6 import (
    QtWidgets as qtw,
    QtCore as qtc,
    QtGui as qtg,
)

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
        """)

        # Songs in playlist view section
        

        # Music folder view section

        # Buttons and progress bar section

        # Combining all layouts and widgets
        main_layout = qtw.QVBoxLayout()
        main_layout.addLayout(layout_walkman_music_folder)
        main_layout.addWidget(self.playlist_section_group)

        self.setLayout(main_layout)

