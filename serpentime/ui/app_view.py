from datetime import date, timedelta

from PyQt5.QtWidgets import (
    QDateEdit, QGraphicsView, QHBoxLayout, QMainWindow, QPushButton,
    QVBoxLayout, QWidget
)
from PyQt5.QtCore import QDate

from .app_model import AppModel


class AppView(QMainWindow):
    """The main window of the app. Displays a chronodex, and allows
    navigation across multiple chronodexes.
    """

    def __init__(self):
        super().__init__()
        self.model = AppModel()
        self.initUI()

    def initUI(self):

        self.prev_week_button = QPushButton("<<")
        self.prev_week_button.clicked.connect(self.on_prev_week_clicked)
        self.prev_day_button = QPushButton("<")
        self.prev_day_button.clicked.connect(self.on_prev_day_clicked)
        self.date_edit = QDateEdit(QDate.currentDate())
        self.date_edit.dateChanged.connect(self.on_date_changed)
        self.next_day_button = QPushButton(">")
        self.next_day_button.clicked.connect(self.on_next_day_clicked)
        self.next_week_button = QPushButton(">>")
        self.next_week_button.clicked.connect(self.on_next_week_clicked)

        date_nav_layout = QHBoxLayout()
        date_nav_layout.addWidget(self.prev_week_button)
        date_nav_layout.addWidget(self.prev_day_button)
        date_nav_layout.addWidget(self.date_edit)
        date_nav_layout.addWidget(self.next_day_button)
        date_nav_layout.addWidget(self.next_week_button)

        self.chronodex_view = QGraphicsView(self.model.chronodex_graph)

        base_layout = QVBoxLayout()
        base_layout.addLayout(date_nav_layout)
        base_layout.addWidget(self.chronodex_view)

        self.main_view = QWidget()
        self.main_view.setLayout(base_layout)

        self.setCentralWidget(self.main_view)

        self.show()

    def on_prev_week_clicked(self):
        new_date = self.model.date - timedelta(days=7)
        self.date_edit.setDate(
            QDate(new_date.year, new_date.month, new_date.day)
        )

    def on_prev_day_clicked(self):
        new_date = self.model.date - timedelta(days=1)
        self.date_edit.setDate(
            QDate(new_date.year, new_date.month, new_date.day)
        )

    def on_date_changed(self, new_date):
        self.model.date = new_date.toPyDate()

    def on_next_day_clicked(self):
        new_date = self.model.date + timedelta(days=1)
        today = date.today()
        if new_date > today:
            new_date = today
        self.date_edit.setDate(
            QDate(new_date.year, new_date.month, new_date.day)
        )

    def on_next_week_clicked(self):
        new_date = self.model.date + timedelta(days=7)
        today = date.today()
        if new_date > today:
            new_date = today
        self.date_edit.setDate(
            QDate(new_date.year, new_date.month, new_date.day)
        )
