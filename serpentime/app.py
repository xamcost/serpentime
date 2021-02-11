import sys
from PyQt5.QtWidgets import QApplication

from .ui.app_view import AppView


def main():
    app = QApplication(sys.argv)
    _ = AppView()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
