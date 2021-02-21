import sys
import pkg_resources
from unittest import mock, TestCase

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtTest import QTest

from serpentime.ui.app_view import AppView
from serpentime.core.chronodex import Chronodex


DATA_PATH = pkg_resources.resource_filename("serpentime.files", "data")

app = QApplication(sys.argv)


class TestAppView(TestCase):
    """Test the app GUI"""

    def setUp(self):
        """Create the GUI"""
        self.view = AppView()

    def test_date_navigation(self):
        """Checks that button in the navigation bar updates the date in
        the drop-down and calendar accordingly.
        """
        self.set_load_save_mocks()
        # When
        self.view.model.auto_save = False
        # Then
        with self.subTest("Start with today's date set"):
            today = QDate.currentDate()
            self.check_on_date_changed(today, check_get=False, auto_save=False)

        self.check_date_nav_buttons(self.view.model.auto_save)

        # When
        self.view.model.auto_save = True
        # Then
        self.check_date_nav_buttons(self.view.model.auto_save)

    def check_date_nav_buttons(self, auto_save):
        """Tests the date navigation buttons.
        """
        today = QDate.currentDate()
        with self.subTest("Testing buttons in the navigation bar"):
            QTest.mouseClick(self.view.prev_week_button, Qt.LeftButton)
            self.check_on_date_changed(today.addDays(-7), auto_save=auto_save)

            QTest.mouseClick(self.view.prev_day_button, Qt.LeftButton)
            self.check_on_date_changed(today.addDays(-8), auto_save=auto_save)

            QTest.mouseClick(self.view.next_day_button, Qt.LeftButton)
            self.check_on_date_changed(today.addDays(-7), auto_save=auto_save)

            QTest.mouseClick(self.view.next_week_button, Qt.LeftButton)
            self.check_on_date_changed(today, auto_save=auto_save)

            # Hitting next day/week buttons should not increase the date
            # later than the current one.
            QTest.mouseClick(self.view.next_day_button, Qt.LeftButton)
            self.check_on_date_changed(
                today, check_get=False, auto_save=False
            )
            self.mk_get_chrono.assert_not_called()

            QTest.mouseClick(self.view.next_week_button, Qt.LeftButton)
            self.check_on_date_changed(
                today, check_get=False, auto_save=False
            )
            self.mk_get_chrono.assert_not_called()

    def set_load_save_mocks(self):
        """Creates mocks for AppModel.get_chronodex and AppView.save_chronodex
        to prevent interactions of AppView with files stored in files/data/.
        """
        self.mk_get_chrono = mock.Mock(return_value=Chronodex())
        self.view.model.get_chronodex = self.mk_get_chrono

        self.mk_save_chrono = mock.Mock()
        self.view.save_chronodex = self.mk_save_chrono

    def check_on_date_changed(self, date, check_get=True, auto_save=True):
        """Checks that calendar and date_edit widgets are set to the given
        date.
        """
        self.assertEqual(self.view.date_edit.date(), date)
        self.assertEqual(self.view.calendar_widget.selectedDate(), date)
        if check_get:
            self.mk_get_chrono.assert_called_once_with(date.toPyDate())
            self.mk_get_chrono.reset_mock()
        if auto_save:
            self.mk_save_chrono.assert_called_once()
            self.mk_save_chrono.reset_mock()
        else:
            self.mk_save_chrono.assert_not_called()
