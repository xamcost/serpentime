import pkg_resources
import os
import csv
from datetime import date

from serpentime.core.chronodex import Chronodex

from .chronodex_graph import ChronodexGraph
from .chronodex_table_model import ChronodexTableModel


FILE_PATH = pkg_resources.resource_filename("serpentime.files", "data")


class AppModel(object):

    def __init__(self):
        self.txt_file_list = []
        self.csv_file_list = []
        for fi in os.listdir(FILE_PATH):
            if fi.endswith('.txt'):
                self.txt_file_list.append(fi)
            elif fi.endswith('.csv'):
                self.csv_file_list.append(fi)
        self._date = date.today()
        self._chronodex = self.get_chronodex(self._date)
        self.chronodex_graph = ChronodexGraph(self.chronodex)
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

    def get_chronodex(self, date):
        basename = date.isoformat().replace('-', '')
        csvname = basename + '.csv'
        txtname = basename + '.txt'
        if csvname in self.csv_file_list:
            return Chronodex.from_csv(os.path.join(FILE_PATH, csvname))
        elif txtname in self.txt_file_list:
            return Chronodex.from_txt(os.path.join(FILE_PATH, txtname))
        return Chronodex()

    def load_chronodex(self, filename):
        if filename.endswith(".txt"):
            self.model.chronodex = Chronodex.from_txt(filename)
        elif filename.endswith(".csv"):
            self.model.chronodex = Chronodex.from_csv(filename)

    def save_chronodex(self):
        filename = self._date.isoformat().replace('-', '') + '.csv'
        with open(os.path.join(FILE_PATH, filename), 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            for act in self.chronodex.activities:
                writer.writerow(
                    [act.start, act.end, act.category, act.name, act.weight]
                )


if __name__ == "__main__":
    model = AppModel()
