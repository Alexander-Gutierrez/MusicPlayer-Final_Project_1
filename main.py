from PyQt6 import QtCore, QtGui, QtWidgets
import sys
from PyQt6.QtWidgets import QApplication, QWidget
from Logic import *


def main():
    app = QApplication(sys.argv)

    window = Logic()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()