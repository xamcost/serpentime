import pkg_resources
import os
from datetime import date, timedelta

from PyQt5.QtWidgets import (
    QAction, QCalendarWidget, QDateEdit, QDockWidget, QFileDialog,
    QGraphicsView, QHBoxLayout, QMainWindow, QPushButton, QTableView,
    QVBoxLayout, QWidget
)
from PyQt5.QtCore import QDate, QModelIndex, Qt
from PyQt5.QtGui import QIcon

from serpentime.core.chronodex import Chronodex

from .app_model import AppModel


ICON_PATH = pkg_resources.resource_filename("serpentime.ui", "icons")


class AppView(QMainWindow):
    """The main window of the app. Displays a chronodex, and allows
    navigation across multiple chronodexes.
    """

    def __init__(self):
        super().__init__()
        self.model = AppModel()
        self.initUI()

    def initUI(self):
        # Sets up the date navigation bar on top of the Chronodex graph
        self.pref_dock_button = QPushButton("\u25C0")
        self.pref_dock_button.clicked.connect(self.toogle_pref_pane)
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
        self.table_dock_button = QPushButton("\u25B6")
        self.table_dock_button.clicked.connect(self.toogle_table_pane)

        date_nav_layout = QHBoxLayout()
        date_nav_layout.addWidget(self.pref_dock_button)
        date_nav_layout.addWidget(self.prev_week_button)
        date_nav_layout.addWidget(self.prev_day_button)
        date_nav_layout.addWidget(self.date_edit)
        date_nav_layout.addWidget(self.next_day_button)
        date_nav_layout.addWidget(self.next_week_button)
        date_nav_layout.addWidget(self.table_dock_button)

        # Sets up the Chronodex graph as the main widget
        self.chronodex_view = QGraphicsView(self.model.chronodex_graph)
        base_layout = QVBoxLayout()
        base_layout.addLayout(date_nav_layout)
        base_layout.addWidget(self.chronodex_view)

        self.main_view = QWidget(self)
        self.main_view.setLayout(base_layout)
        self.setCentralWidget(self.main_view)

        # Sets up the left dock pane for the calendar and table
        self.table_dock = QDockWidget(self)
        self.calendar_widget = QCalendarWidget()
        self.calendar_widget.clicked.connect(self.on_date_changed)
        self.add_row_button = QPushButton(
            QIcon(os.path.join(ICON_PATH, "add-black-18dp.svg")), ""
        )
        self.add_row_button.clicked.connect(self.add_activity)
        self.del_row_button = QPushButton(
            QIcon(os.path.join(ICON_PATH, "remove-black-18dp.svg")), ""
        )
        self.del_row_button.clicked.connect(self.remove_selected_activities)
        self.load_button = QPushButton(
            QIcon(os.path.join(ICON_PATH, "download-black-18dp.svg")), ""
        )
        self.load_button.clicked.connect(self.load_chronodex)
        self.save_button = QPushButton(
            QIcon(os.path.join(ICON_PATH, "save-black-18dp.svg")), ""
        )
        self.table_view = QTableView()
        self.table_view.setModel(self.model.chronodex_table)
        self.table_view.resizeColumnsToContents()
        self.model.chronodex_table.dataChanged.connect(self.on_activity_edited)

        table_button_layout = QHBoxLayout()
        table_button_layout.addWidget(self.add_row_button)
        table_button_layout.addWidget(self.del_row_button)
        table_button_layout.addStretch()
        table_button_layout.addWidget(self.load_button)
        table_button_layout.addWidget(self.save_button)

        right_dock_layout = QVBoxLayout()
        right_dock_layout.addWidget(self.calendar_widget)
        right_dock_layout.addLayout(table_button_layout)
        right_dock_layout.addWidget(self.table_view)
        right_dock_widget = QWidget()
        right_dock_widget.setLayout(right_dock_layout)
        self.table_dock.setWidget(right_dock_widget)
        self.addDockWidget(Qt.RightDockWidgetArea, self.table_dock)

        # Sets up menus
        menubar = self.menuBar()
        # menubar.setNativeMenuBar(False)
        view_menu = menubar.addMenu('View')
        table_pane_visibility = QAction('Table pane', self, checkable=True)
        table_pane_visibility.setStatusTip('Calendar and table pane')
        table_pane_visibility.setChecked(True)
        table_pane_visibility.triggered.connect(self.toogle_table_pane)
        view_menu.addAction(table_pane_visibility)

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
        self.calendar_widget.setSelectedDate(new_date)
        # Disconnect and then reconnect dateChanged to avoid multiple calls
        # to this slot
        self.date_edit.dateChanged.disconnect()
        self.date_edit.setDate(new_date)
        self.date_edit.dateChanged.connect(self.on_date_changed)
        self.table_view.resizeColumnsToContents()

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

    def on_activity_edited(self, top_left, bottom_right):
        self.model.chronodex_graph.draw_chronodex()

    def toogle_table_pane(self):
        visible = self.table_dock.isVisible()
        self.table_dock.setVisible(not visible)
        if visible:
            self.table_dock_button.setText("\u25C0")
        else:
            self.table_dock_button.setText("\u25B6")

    def toogle_pref_pane(self):
        pass

    def add_activity(self):
        selected = self.table_view.selectedIndexes()
        row_indexes = [ind.row() for ind in selected]
        if len(row_indexes) > 0:
            pos = max(row_indexes) + 1
        else:
            pos = self.model.chronodex_table.rowCount(None)
        self.model.chronodex_table.insertRows(pos, 1, QModelIndex())

    def remove_selected_activities(self):
        selected = self.table_view.selectedIndexes()
        row_indexes = reversed(sorted(set([ind.row() for ind in selected])))
        for ind in row_indexes:
            self.model.chronodex_table.removeRow(ind, QModelIndex())
        self.model.chronodex_graph.draw_chronodex()

    def load_chronodex(self):
        filename, _ = QFileDialog.getOpenFileName(
            self, "Select file containing chronodex info",
            os.path.expanduser("~"), "(*.txt *.csv)",
        )
        self.model.chronodex = Chronodex.from_file(filename)
