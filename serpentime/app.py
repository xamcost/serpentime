import sys
from PyQt5.QtWidgets import QApplication

from .ui.main_window import MainWindow


def main(path=None):
    app = QApplication(sys.argv)
    _ = MainWindow(path)
    sys.exit(app.exec_())


if __name__ == "__main__":
    import os
    this_dir = os.path.dirname(__file__)
    main(os.path.join(this_dir, 'files', 'data', '20191113.txt'))
