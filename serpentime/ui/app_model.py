import pkg_resources
import os
import csv
import json
from datetime import date

from serpentime.core.chronodex import Chronodex

from .chronodex_graph import ChronodexGraph
from .chronodex_table_model import ChronodexTableModel
from .pref_table_model import PrefTableModel


PREF_PATH = os.path.join(
    pkg_resources.resource_filename("serpentime", "files"), "preferences.json"
)
DATA_PATH = pkg_resources.resource_filename("serpentime.files", "data")


class AppModel(object):
    """The application model for the Serpentime UI.
    """

    def __init__(self):
        """Initialises the application model by loading today's chronodex.
        If none exists, creates an empty chronodex ready to be edited.
        """
        self.txt_file_list = []
        self.csv_file_list = []
        for fi in os.listdir(DATA_PATH):
            if fi.endswith('.txt'):
                self.txt_file_list.append(fi)
            elif fi.endswith('.csv'):
                self.csv_file_list.append(fi)
        self._date = date.today()
        self._chronodex = self.get_chronodex(self._date)
        self._preferences = self.load_preferences()
        self.pref_table = PrefTableModel(preferences=self._preferences)
        self.chronodex_graph = ChronodexGraph(
            self.chronodex, self._preferences
        )
        self.chronodex_table = ChronodexTableModel(self.chronodex)

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        self._date = value
        self.chronodex = self.get_chronodex(value)

    @property
    def chronodex(self):
        return self._chronodex

    @chronodex.setter
    def chronodex(self, value):
        self._chronodex = value
        self.chronodex_graph.chronodex = self._chronodex
        self.chronodex_table.chronodex = self._chronodex

    @property
    def preferences(self):
        return self._preferences

    @preferences.setter
    def preferences(self, value):
        self._preferences = value
        self.pref_table.preferences = self._preferences
        self.chronodex_graph.preferences = self._preferences

    @property
    def show_labels(self):
        return self._preferences.get("show_labels", False)

    @show_labels.setter
    def show_labels(self, value):
        self._preferences["show_labels"] = value
        self.chronodex_graph.preferences = self._preferences

    @property
    def rotate_labels(self):
        return self._preferences.get("rotate_labels", False)

    @rotate_labels.setter
    def rotate_labels(self, value):
        self._preferences["rotate_labels"] = value
        self.chronodex_graph.preferences = self._preferences

    @property
    def show_overlay(self):
        return self._preferences.get("show_overlay", False)

    @show_overlay.setter
    def show_overlay(self, value):
        self._preferences["show_overlay"] = value
        self.chronodex_graph.preferences = self._preferences

    @property
    def use_custom_weight(self):
        return self._preferences.get("use_custom_weight", False)

    @use_custom_weight.setter
    def use_custom_weight(self, value):
        self._preferences["use_custom_weight"] = value
        self.chronodex_graph.preferences = self._preferences

    @property
    def auto_save(self):
        return self._preferences.get("auto_save", False)

    @auto_save.setter
    def auto_save(self, value):
        self._preferences["auto_save"] = value
        self.chronodex_graph.preferences = self._preferences

    @property
    def categories(self):
        return [cat['name'] for cat in self.pref_table.categories]

    def get_chronodex(self, date):
        """Returns the Chronodex instances for the given date.

        Parameters
        ----------
        date: datetime.Date
            The date corresponding to the Chronodex to be returned.

        Returns
        -------
        chronodex: serpentime.core.Chronodex
            The Chronodex instance corresponding to the given date.
        """
        basename = date.isoformat().replace('-', '')
        csvname = basename + '.csv'
        txtname = basename + '.txt'
        if csvname in self.csv_file_list:
            return Chronodex.from_csv(os.path.join(DATA_PATH, csvname))
        elif txtname in self.txt_file_list:
            return Chronodex.from_txt(os.path.join(DATA_PATH, txtname))
        return Chronodex()

    def load_chronodex(self, filename):
        """Assigns a Chronodex loaded from the given filename to
        :attr:`chronodex`.

        Parameters
        ----------
        filename: str
            The full name of the file containing the chronodex data.
        """
        if filename.endswith(".txt"):
            self.chronodex = Chronodex.from_txt(filename)
        elif filename.endswith(".csv"):
            self.chronodex = Chronodex.from_csv(filename)

    def save_chronodex(self):
        """Saves the chronodex data in a csv file.
        """
        filename = self._date.isoformat().replace('-', '') + '.csv'
        with open(os.path.join(DATA_PATH, filename), 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            for act in self.chronodex.activities:
                if act.is_valid():
                    writer.writerow(
                        [act.start, act.end, act.category,
                         act.name, act.weight]
                    )
        if filename not in self.csv_file_list:
            self.csv_file_list.append(filename)

    def delete_chronodex(self):
        """Deletes the chronodex file corresponding to :attr:`date`.
        """
        basename = self._date.isoformat().replace('-', '')
        csvname = basename + '.csv'
        txtname = basename + '.txt'
        if csvname in self.csv_file_list:
            os.remove(os.path.join(DATA_PATH, csvname))
            self.csv_file_list.remove(csvname)
        if txtname in self.txt_file_list:
            os.remove(os.path.join(DATA_PATH, txtname))
            self.txt_file_list.remove(txtname)
        self.chronodex = Chronodex()

    def load_preferences(self):
        """Assigns to :attr:`preferences` the loaded preferences dictionary
        from serpentime/files/preferences.json
        """
        with open(PREF_PATH, 'r') as fi:
            preferences = json.load(fi)
        return preferences

    def save_preferences(self):
        """Saves the preferences.
        """
        with open(PREF_PATH, 'w') as fi:
            json.dump(self.preferences, fi)


if __name__ == "__main__":
    model = AppModel()
