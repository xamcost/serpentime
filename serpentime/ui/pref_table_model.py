from PyQt5.QtCore import QAbstractTableModel, Qt
from PyQt5.QtGui import QColor


COLUMNS = [
    ('Category', 'name'),
    ('Color', 'color'),
    ('Weight', 'weight'),
]


class PrefTableModel(QAbstractTableModel):
    """A model for table of category preferences."""

    def __init__(self, preferences={}):
        super().__init__()
        self.preferences = preferences
        self.categories = self.preferences.get("categories", [])

    def data(self, index, role):
        col = COLUMNS[index.column()][1]
        category = self.categories[index.row()]
        if role == Qt.DisplayRole or role == Qt.EditRole:
            return category.get(col, "")
        if role == Qt.DecorationRole:
            if col == "color":
                return QColor(category.get(col, "#00FFFFFF"))

    def setData(self, index, value, role):
        if role == Qt.EditRole:
            col = COLUMNS[index.column()][1]
            category = self.categories[index.row()]
            category[col] = value
            self.dataChanged.emit(index, index)
            return True

    def insertRows(self, pos, count, index):
        self.beginInsertRows(index, pos, pos + count - 1)
        for ind in range(pos, pos + count):
            self.categories.insert(ind, {})
        self.endInsertRows()
        return True

    def removeRows(self, pos, count, index):
        self.beginRemoveRows(index, pos, pos + count - 1)
        for ind in range(pos, pos + count):
            self.categories.pop(pos)
        self.endRemoveRows()
        return True

    def flags(self, index):
        return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return COLUMNS[section][0]
        return super().headerData(section, orientation, role)

    def rowCount(self, index):
        return len(self.categories)

    def columnCount(self, index):
        return len(COLUMNS)
