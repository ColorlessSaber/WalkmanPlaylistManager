from PySide6 import QtWidgets as qtw

class ModifiedQComboBox(qtw.QComboBox):

    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)

    def all_items(self) -> list:
        """
        Returns a list of all items in the QComboBox.

        :return: List of all items in the QComboBox.
        """
        return [self.itemText(index) for index in range(self.count())]