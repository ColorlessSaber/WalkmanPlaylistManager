from PySide6 import QtWidgets as qtw

class ModifiedQComboBox(qtw.QComboBox):

    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)

    def remove_item(self, item_name: str) -> None:
        """
        Removes an item from the QComboBox and sets current index to zero after changes.

        :param item_name: Name of the item to remove
        :return:
        """
        item_list = self.all_items()
        item_list.remove(item_name)

        self.clear()
        self.addItems(item_list)

    def all_items(self) -> list:
        """
        Returns a list of all items in the QComboBox.

        :return: List of all items in the QComboBox.
        """
        return [self.itemText(index) for index in range(self.count())]