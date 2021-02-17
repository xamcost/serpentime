from PyQt5.QtWidgets import QComboBox, QDoubleSpinBox, QStyledItemDelegate
from PyQt5.QtCore import Qt


class SpinBoxDelegate(QStyledItemDelegate):

    def __init__(self, owner, minimum, maximum, step=1):
        super().__init__(owner)
        self.range = (minimum, maximum)
        self.step = step

    # def paint(self, painter, option, index):
    #     if isinstance(self.parent(), QAbstractItemView):
    #         self.parent().openPersistentEditor(index)
    #     super().paint(painter, option, index)

    def createEditor(self, parent, option, index):
        editor = QDoubleSpinBox(parent)
        # editor.currentIndexChanged.connect(self.commit_editor)
        editor.setRange(*self.range)
        editor.setSingleStep(self.step)
        return editor

    # def commit_editor(self):
    #     editor = self.sender()
    #     self.commitData.emit(editor)

    def setEditorData(self, editor, index):
        value = index.data(Qt.EditRole)
        if isinstance(value, (int, float)):
            editor.setValue(value)

    def setModelData(self, editor, model, index):
        value = editor.value()
        model.setData(index, value, Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)


class ComboBoxDelegate(QStyledItemDelegate):

    def __init__(self, owner, choices):
        super().__init__(owner)
        self.items = choices

    # def paint(self, painter, option, index):
    #     if isinstance(self.parent(), QAbstractItemView):
    #         self.parent().openPersistentEditor(index)
    #     super().paint(painter, option, index)

    def createEditor(self, parent, option, index):
        editor = QComboBox(parent)
        # editor.currentIndexChanged.connect(self.commit_editor)
        editor.addItems(self.items)
        return editor

    # def commit_editor(self):
    #     editor = self.sender()
    #     self.commitData.emit(editor)

    def setEditorData(self, editor, index):
        value = index.data(Qt.DisplayRole)
        if value in self.items:
            num = self.items.index(value)
            editor.setCurrentIndex(num)

    def setModelData(self, editor, model, index):
        value = editor.currentText()
        model.setData(index, value, Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)
