from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QListWidget


class CustomList(QListWidget):
    def sizeHint(self):
        s = QSize()
        s.setHeight(super(CustomList, self).sizeHint().height())
        s.setWidth(self.sizeHintForColumn(0) + 25)
        return s
