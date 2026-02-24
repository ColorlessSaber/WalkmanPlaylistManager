from PySide6 import QtCore as qtc
from typing import Any
from .generic_pyside_objects import GenericTable

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