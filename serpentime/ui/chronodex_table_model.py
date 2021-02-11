from PyQt5 import QtCore


COLUMNS = [
    ('Start Time', 'start_time'),
    ('End Time', 'end_time'),
    ('Category', 'category'),
    ('Name', 'name'),
]


class ChronodexTableModel(QtCore.QAbstractTableModel):
    """A model for the table of activities constituting the Chronodex."""

    def __init__(self, chronodex):
        super().__init__()
        self.chronodex = chronodex

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            activity = self.chronodex.activities[index.row()]
            attr_name = COLUMNS[index.column()][1]
            return getattr(activity, attr_name)

    def rowCount(self, index):
        return len(self.chronodex.activities)

    def columnCount(self, index):
        return len(self.chronodex.activities[0])
