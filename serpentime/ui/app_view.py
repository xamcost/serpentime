import pkg_resources
import os
from datetime import date, timedelta

from PyQt5.QtWidgets import (
    QAction, QCalendarWidget, QCheckBox, QDateEdit, QDockWidget, QFileDialog,
    QGraphicsView, QHBoxLayout, QMainWindow, QMenu, QPushButton, QTableView,
    QVBoxLayout, QWidget
)
from PyQt5.QtCore import QDate, QModelIndex, Qt
from PyQt5.QtGui import QIcon

from .app_model import AppModel
from .item_delegates import ComboBoxDelegate, SpinBoxDelegate


ICON_PATH = pkg_resources.resource_filename("serpentime.ui", "icons")


class AppView(QMainWindow):
    """The main window of the app. Displays a chronodex, and allows
    navigation across multiple chronodexes.
    """

    def __init__(self):
        super().__init__()
        self.model = AppModel()
        self.col_names = [col[0] for col in self.model.chronodex_table.columns]
        self.initUI()

    def initUI(self):
        # Sets up the central widget: date navigation bar and graph
        date_nav_layout = self.create_date_navigation_bar()

        self.chronodex_view = QGraphicsView(self.model.chronodex_graph)
        base_layout = QVBoxLayout()
        base_layout.addLayout(date_nav_layout)
        base_layout.addWidget(self.chronodex_view)

        self.main_view = QWidget(self)
        self.main_view.setLayout(base_layout)
        self.setCentralWidget(self.main_view)

        # Sets up the table dock pane for the calendar and table
        self.table_dock = QDockWidget(self)
        self.calendar_widget = QCalendarWidget()
        self.calendar_widget.clicked.connect(self.on_date_changed)
        self.table_view = self.create_chronodex_table()
        self.model.chronodex_table.dataChanged.connect(self.on_activity_edited)

        table_button_layout = self.create_chronodex_table_button_bar()

        right_dock_layout = QVBoxLayout()
        right_dock_layout.addWidget(self.calendar_widget)
        right_dock_layout.addLayout(table_button_layout)
        right_dock_layout.addWidget(self.table_view)
        right_dock_widget = QWidget()
        right_dock_widget.setLayout(right_dock_layout)
        self.table_dock.setWidget(right_dock_widget)
        self.addDockWidget(Qt.RightDockWidgetArea, self.table_dock)

        # Sets up the preferences dock pane
        self.pref_dock = QDockWidget(self)
        self.add_category_button = QPushButton(
            QIcon(os.path.join(ICON_PATH, "add-black-18dp.svg")), ""
        )
        self.add_category_button.clicked.connect(self.add_category)
        self.del_category_button = QPushButton(
            QIcon(os.path.join(ICON_PATH, "remove-black-18dp.svg")), ""
        )
        self.del_category_button.clicked.connect(
            self.remove_selected_categories
        )
        self.save_pref_button = QPushButton(
            QIcon(os.path.join(ICON_PATH, "save-black-18dp.svg")), ""
        )
        self.save_pref_button.clicked.connect(self.save_preferences)
        self.pref_table_view = self.create_pref_table()
        self.model.pref_table.dataChanged.connect(self.on_pref_edited)
        self.show_labels_checkbox = QCheckBox("Show labels")
        self.show_labels_checkbox.setChecked(self.model.show_labels)
        self.show_labels_checkbox.setToolTip(
            "If checked, activity names are displayed on Chronodex graph."
        )
        self.show_labels_checkbox.stateChanged.connect(self.set_show_labels)
        self.rotate_checkbox = QCheckBox("Rotate labels")
        self.rotate_checkbox.setChecked(self.model.rotate_labels)
        self.rotate_checkbox.setToolTip(
            "If checked, activity names are titled."
        )
        self.rotate_checkbox.stateChanged.connect(
            self.set_activity_name_rotation
        )
        self.rotate_checkbox.setEnabled(
            self.model.preferences.get(
                "show_labels", self.show_labels_checkbox.isChecked()
            )
        )
        self.overlay_checkbox = QCheckBox("Show overlay")
        self.overlay_checkbox.setChecked(self.model.show_overlay)
        self.overlay_checkbox.setToolTip(
            "If checked, displays overlay circles on Chronodex graph."
        )
        self.overlay_checkbox.stateChanged.connect(
            self.set_show_overlay
        )
        self.weight_checkbox = QCheckBox("Use custom weight")
        self.weight_checkbox.setChecked(self.model.use_custom_weight)
        self.weight_checkbox.setToolTip(
            "If checked, weights are taken from chronodex table, not from "
            "preferences table above."
        )
        self.weight_checkbox.stateChanged.connect(self.set_custom_weight)
        self.auto_save_checkbox = QCheckBox("Auto save")
        self.auto_save_checkbox.setChecked(self.model.auto_save)
        self.auto_save_checkbox.setToolTip(
            "If checked, the current chronodex will be automatically "
            "saved for each edition of its table, or when the date is changed."
        )
        self.auto_save_checkbox.stateChanged.connect(self.set_auto_save)

        pref_table_button_layout = QHBoxLayout()
        pref_table_button_layout.addWidget(self.add_category_button)
        pref_table_button_layout.addWidget(self.del_category_button)
        pref_table_button_layout.addStretch()
        pref_table_button_layout.addWidget(self.save_pref_button)

        pref_dock_layout = QVBoxLayout()
        pref_dock_layout.addLayout(pref_table_button_layout)
        pref_dock_layout.addWidget(self.pref_table_view)
        pref_dock_layout.addWidget(self.show_labels_checkbox)
        pref_dock_layout.addWidget(self.rotate_checkbox)
        pref_dock_layout.addWidget(self.overlay_checkbox)
        pref_dock_layout.addWidget(self.weight_checkbox)
        pref_dock_layout.addWidget(self.auto_save_checkbox)
        pref_dock_widget = QWidget()
        pref_dock_widget.setLayout(pref_dock_layout)
        self.pref_dock.setWidget(pref_dock_widget)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.pref_dock)

        # Sets up menus
        menubar = self.menuBar()
        # menubar.setNativeMenuBar(False)
        view_menu = menubar.addMenu('&View')
        self.toggle_table_pane_action = QAction(
            'Table pane', self, checkable=True
        )
        self.toggle_table_pane_action.setStatusTip('Calendar and table pane')
        self.toggle_table_pane_action.setChecked(True)
        self.toggle_table_pane_action.triggered.connect(self.toogle_table_pane)
        view_menu.addAction(self.toggle_table_pane_action)
        self.toggle_pref_pane_action = QAction(
            'Chronodex pane', self, checkable=True
        )
        self.toggle_pref_pane_action.setStatusTip('Preferences pane')
        self.toggle_pref_pane_action.setChecked(True)
        self.toggle_pref_pane_action.triggered.connect(self.toogle_pref_pane)
        view_menu.addAction(self.toggle_pref_pane_action)

        # Sets general config of UI
        self.setGeometry(100, 100, 1200, 700)
        self.setWindowTitle("Serpentime")

        self.show()

    def create_date_navigation_bar(self):
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

        return date_nav_layout

    def create_chronodex_table_button_bar(self):
        self.add_row_button = QPushButton(
            QIcon(os.path.join(ICON_PATH, "add-black-18dp.svg")), ""
        )
        self.add_row_button.clicked.connect(self.add_activity)
        self.del_row_button = QPushButton(
            QIcon(os.path.join(ICON_PATH, "remove-black-18dp.svg")), ""
        )
        self.del_row_button.clicked.connect(self.remove_selected_activities)
        self.del_button = QPushButton(
            QIcon(os.path.join(ICON_PATH, "delete-black-18dp.svg")), ""
        )
        self.del_button.clicked.connect(self.delete_chronodex)
        self.load_button = QPushButton(
            QIcon(os.path.join(ICON_PATH, "download-black-18dp.svg")), ""
        )
        self.load_button.clicked.connect(self.load_chronodex)
        self.save_button = QPushButton(
            QIcon(os.path.join(ICON_PATH, "save-black-18dp.svg")), ""
        )
        self.save_button.clicked.connect(self.save_chronodex)

        table_button_layout = QHBoxLayout()
        table_button_layout.addWidget(self.add_row_button)
        table_button_layout.addWidget(self.del_row_button)
        table_button_layout.addStretch()
        table_button_layout.addWidget(self.del_button)
        table_button_layout.addWidget(self.load_button)
        table_button_layout.addWidget(self.save_button)

        return table_button_layout

    def create_chronodex_table(self):
        table_view = QTableView()
        table_view.setModel(self.model.chronodex_table)
        start_index = self.col_names.index('Start')
        table_view.setItemDelegateForColumn(
            start_index, SpinBoxDelegate(table_view, 0, 23.99),
        )
        end_index = self.col_names.index('End')
        table_view.setItemDelegateForColumn(
            end_index, SpinBoxDelegate(table_view, 0.01, 24),
        )
        self.category_delegate = ComboBoxDelegate(
            table_view, self.model.categories
        )
        table_view.setItemDelegateForColumn(
            self.col_names.index('Category'), self.category_delegate
        )
        weight_index = self.col_names.index('Weight')
        table_view.setItemDelegateForColumn(
            weight_index, SpinBoxDelegate(table_view, 0, 10),
        )
        table_view.setColumnWidth(start_index, 50)
        table_view.setColumnWidth(end_index, 50)
        use_custom_weight = self.model.preferences.get(
            'use_custom_weight', False
        )
        table_view.setColumnHidden(weight_index, not use_custom_weight)
        table_view.setContextMenuPolicy(Qt.CustomContextMenu)
        table_view.customContextMenuRequested.connect(self.open_table_menu)
        return table_view

    def create_pref_table(self):
        pref_table = QTableView()
        pref_table.setModel(self.model.pref_table)
        pref_table.resizeColumnsToContents()
        return pref_table

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
        # Saves the chronodex before changing page
        if self.model.auto_save:
            self.save_chronodex()
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

    def on_pref_edited(self, top_left, bottom_right):
        self.model.preferences = self.model.pref_table.preferences
        self.category_delegate.items = self.model.categories

    def toogle_table_pane(self):
        visible = self.table_dock.isVisible()
        self.table_dock.setVisible(not visible)
        self.toggle_table_pane_action.setChecked(not visible)
        if visible:
            self.table_dock_button.setText("\u25C0")
        else:
            self.table_dock_button.setText("\u25B6")

    def toogle_pref_pane(self):
        visible = self.pref_dock.isVisible()
        self.pref_dock.setVisible(not visible)
        self.toggle_pref_pane_action.setChecked(not visible)
        if visible:
            self.pref_dock_button.setText("\u25B6")
        else:
            self.pref_dock_button.setText("\u25C0")

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
        self.model.load_chronodex(filename)

    def save_chronodex(self):
        if len(self.model.chronodex.activities) > 0:
            self.model.save_chronodex()

    def delete_chronodex(self):
        self.model.delete_chronodex()

    def add_category(self):
        selected = self.pref_table_view.selectedIndexes()
        row_indexes = [ind.row() for ind in selected]
        if len(row_indexes) > 0:
            pos = max(row_indexes) + 1
        else:
            pos = self.model.pref_table.rowCount(None)
        self.model.pref_table.insertRows(pos, 1, QModelIndex())

    def remove_selected_categories(self):
        selected = self.pref_table_view.selectedIndexes()
        row_indexes = reversed(sorted(set([ind.row() for ind in selected])))
        for ind in row_indexes:
            self.model.pref_table.removeRow(ind, QModelIndex())
        self.model.chronodex_graph.draw_chronodex()

    def save_preferences(self):
        self.model.save_preferences()

    def set_show_labels(self, state):
        self.model.show_labels = state == Qt.Checked
        self.rotate_checkbox.setEnabled(self.model.show_labels)

    def set_activity_name_rotation(self, state):
        self.model.rotate_labels = state == Qt.Checked

    def set_show_overlay(self, state):
        self.model.show_overlay = state == Qt.Checked

    def set_custom_weight(self, state):
        self.model.use_custom_weight = state == Qt.Checked
        self.table_view.setColumnHidden(
            self.col_names.index('Weight'), not self.model.use_custom_weight
        )

    def set_auto_save(self, state):
        self.model.auto_save = state == Qt.Checked

    def open_table_menu(self, pos):
        menu = QMenu()

        insert_above = QAction('Insert above', self)
        insert_above.triggered.connect(self.insert_row_above)

        insert_below = QAction('Insert below', self)
        insert_below.triggered.connect(self.add_activity)

        remove = QAction('Remove', self)
        remove.triggered.connect(self.remove_selected_activities)

        menu.addAction(insert_above)
        menu.addAction(insert_below)
        menu.addAction(remove)
        menu.exec_(self.table_view.mapToGlobal(pos))

    def insert_row_above(self):
        selected = self.table_view.selectedIndexes()
        row_indexes = [ind.row() for ind in selected]
        if len(row_indexes) > 0:
            pos = min(row_indexes)
        else:
            pos = self.model.chronodex_table.rowCount(None)
        self.model.chronodex_table.insertRows(pos, 1, QModelIndex())
