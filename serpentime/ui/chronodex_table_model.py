from PyQt5 import QtCore


COLUMNS = [
    ('Start Time', 'start'),
    ('End Time', 'end'),
    ('Category', 'category'),
    ('Name', 'name'),
]


class ChronodexTableModel(QtCore.QAbstractTableModel):
    """A model for the table of activities constituting the Chronodex."""

    def __init__(self, chronodex):
        super().__init__()
        self._chronodex = chronodex

    @property
    def chronodex(self):
        return self._chronodex

    @chronodex.setter
    def chronodex(self, value):
        self._chronodex = value
        # Refreshes the table
        self.layoutChanged.emit()

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            activity = self.chronodex.activities[index.row()]
            attr_name = COLUMNS[index.column()][1]
            return getattr(activity, attr_name)

    def rowCount(self, index):
        return len(self.chronodex.activities)

    def columnCount(self, index):
        return len(COLUMNS)
