import sys

from PyQt5.QtWidgets import *

from Source.UI.MainWindow import MainWindow


def main():
    sys.setrecursionlimit(2350)
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
