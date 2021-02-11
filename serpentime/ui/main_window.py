from PyQt5.QtWidgets import QGraphicsView, QMainWindow

from serpentime.core.chronodex import Chronodex

from .chronodex_graph import ChronodexGraph


class MainWindow(QMainWindow):
    """The main window of the app. Displays a chronodex, and allows
    navigation across multiple chronodexes.
    """

    def __init__(self, path):
        super().__init__()
        self.chronodex = Chronodex.from_file(path)
        self.initUI()

    def initUI(self):
        self.chronodex_graph = ChronodexGraph(self.chronodex)
        self.chronodex_view = QGraphicsView(self.chronodex_graph)

        self.setCentralWidget(self.chronodex_view)

        self.show()
