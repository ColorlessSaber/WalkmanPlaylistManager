from typing import Optional
from PySide6 import QtCore as qtc

class GenericTable(qtc.QAbstractTableModel):
    """
    A generic Pyside table object.
    Able to handle any number of columns and rows, specify read-only indexes, and take in names for the columns.
    """

    def __init__(self, read_only_columns: Optional[list] = None, current_media_file_list: Optional[list] = None, column_names: Optional[list] = None):
        super().__init__()
        self._read_only_columns = read_only_columns if read_only_columns is not None else []
        self._data = current_media_file_list if current_media_file_list is not None else []
        self._headers = column_names if column_names is not None else []

        # Validate that the number of columns in the data match the number of provided
        # column names. If not, generate generic names for the missing columns.
        if self._data:
            if len(self._data[0]) != len(self._headers):
                self._headers.extend([f'column_{i}' for i in range(len(self._headers), len(self._data[0]))])

    def rowCount(self, parent=qtc.QModelIndex()) -> int:
        """Return the number of rows in the table"""
        return len(self._data)

    def columnCount(self, parent=qtc.QModelIndex()) -> int:
        """Return the number of columns in the table"""
        return len(self._headers) if self._headers else 0

    def data(self, index, role=qtc.Qt.ItemDataRole.DisplayRole) -> object | None:
        """Return the data at the given index for display and editing"""
        if not index.isValid():
            return None

        if role in (qtc.Qt.ItemDataRole.DisplayRole, qtc.Qt.ItemDataRole.EditRole):
            return self._data[index.row()][index.column()]

        return None

    def setData(self, index, value, role = qtc.Qt.ItemDataRole.EditRole) -> object | None:
        """Set the data at the given index for editing"""
        if index.isValid() and role == qtc.Qt.ItemDataRole.EditRole:
            self._data[index.row()][index.column()] = value
            self.dataChanged.emit(index, index, [role])
            return True
        else:
            return False

    def flags(self, index) -> object:
        """Return the flags attached to the given index"""
        if not index.isValid():
            return qtc.Qt.ItemFlag.ItemIsEnabled

        if index.column() not in self._read_only_columns:
            return super().flags(index) | qtc.Qt.ItemFlag.ItemIsEditable
        else:
            return super().flags(index)

    def headerData(self, section, orientation, role=qtc.Qt.ItemDataRole.DisplayRole) -> object | str | None:
        """Return the header labels"""
        if role == qtc.Qt.ItemDataRole.DisplayRole and orientation == qtc.Qt.Orientation.Horizontal:
            return self._headers[section]
        else:
            return super().headerData(section, orientation, role)

    def insertRows(self, position, rows, parent=qtc.QModelIndex()) -> None:
        """Insert rows into the table"""
        self.beginInsertRows(parent, position, position + rows - 1)
        for i in range(rows):
            default_row = [''] * len(self._headers)
            self._data.insert(position, default_row)
        self.endInsertRows()

    def removeRows(self, position, rows, parent=qtc.QModelIndex()) -> None:
        """Remove rows from the table"""
        self.beginRemoveRows(parent, position, position + rows - 1)
        for i in range(rows):
            del(self._data[position])
        self.endRemoveRows()

    def removeRow(self, position, row=1, parent=qtc.QModelIndex()) -> None:
        """Remove a single row from the table"""
        self.beginRemoveRows(parent, position, position + row - 1)
        del(self._data[position])
        self.endRemoveRows()

    def clear(self) -> None:
        """Clear the table"""
        self.beginResetModel()
        self._data.clear()
        self.endResetModel()
