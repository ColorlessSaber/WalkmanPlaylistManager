"""
The file to start the application
"""
import sys
from PySide6 import QtWidgets as qtw

from src import MainWindow

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec())
