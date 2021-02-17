from PyQt5.QtCore import QAbstractTableModel, Qt

from serpentime.core.chronodex import Activity


COLUMNS = [
    ('Start', 'start'),
    ('End', 'end'),
    ('Category', 'category'),
    ('Name', 'name'),
    ('Weight', 'weight'),
]


class ChronodexTableModel(QAbstractTableModel):
    """A model for the table of activities constituting the Chronodex."""

    def __init__(self, chronodex):
        super().__init__()
        self._chronodex = chronodex
        self.columns = COLUMNS

    @property
    def chronodex(self):
        return self._chronodex

    @chronodex.setter
    def chronodex(self, value):
        self.layoutAboutToBeChanged.emit()
        self._chronodex = value
        # Refreshes the table
        self.layoutChanged.emit()

    def data(self, index, role):
        if role == Qt.DisplayRole or role == Qt.EditRole:
            activity = self.chronodex.activities[index.row()]
            attr_name = self.columns[index.column()][1]
            return getattr(activity, attr_name)

    def setData(self, index, value, role):
        if role == Qt.EditRole:
            activity = self.chronodex.activities[index.row()]
            attr_name = self.columns[index.column()][1]
            try:
                value = float(value)
            except ValueError:
                pass
            setattr(activity, attr_name, value)
            self.dataChanged.emit(index, index)
            return True
        return False

    def insertRows(self, pos, count, index):
        self.beginInsertRows(index, pos, pos + count - 1)
        for ind in range(pos, pos + count):
            start = None
            if ind == 0:
                start = 0
            else:
                prev_end = self.chronodex.activities[ind - 1].end
                if prev_end is not None:
                    start = prev_end
            self.chronodex.activities.insert(ind, Activity(start=start))
        self.endInsertRows()
        return True

    def removeRows(self, pos, count, index):
        self.beginRemoveRows(index, pos, pos + count - 1)
        for ind in range(pos, pos + count):
            self.chronodex.activities.pop(pos)
        self.endRemoveRows()
        return True

    def flags(self, index):
        return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.columns[section][0]
        return super().headerData(section, orientation, role)

    def rowCount(self, index):
        return len(self.chronodex.activities)

    def columnCount(self, index):
        return len(self.columns)
