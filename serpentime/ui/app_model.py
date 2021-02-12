import pkg_resources
import os
from datetime import date

from serpentime.core.chronodex import Chronodex

from .chronodex_graph import ChronodexGraph
from .chronodex_table_model import ChronodexTableModel


FILE_PATH = pkg_resources.resource_filename("serpentime.files", "data")


class AppModel(object):

    def __init__(self):
        self.file_list = [
            fi for fi in os.listdir(FILE_PATH) if fi.endswith('.txt')
        ]
        self._date = date.today()
        self.chronodex = self.get_chronodex(self._date)
        self.chronodex_graph = ChronodexGraph(self.chronodex)
        self.chronodex_table = ChronodexTableModel(self.chronodex)

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        self._date = value
        self.chronodex = self.get_chronodex(value)
        self.chronodex_graph.chronodex = self.chronodex
        self.chronodex_table.chronodex = self.chronodex

    def get_chronodex(self, date):
        filename = date.isoformat().replace('-', '') + '.txt'
        if filename in self.file_list:
            return Chronodex.from_file(os.path.join(FILE_PATH, filename))
        return Chronodex()


if __name__ == "__main__":
    model = AppModel()
