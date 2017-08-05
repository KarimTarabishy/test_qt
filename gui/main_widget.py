from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QGraphicsDropShadowEffect
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QSizePolicy, QStackedLayout, QFrame, QListWidgetItem
from .training_widget import TrainingWidget
from .testing_widget import TestingWidget
from .custom_list import CustomList
from PyQt5 import QtCore


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.list = None
        self.stack = None
        self.init_ui()

    def init_ui(self):
        box = QHBoxLayout()

        self.list = CustomList()
        self.list.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.list.setSelectionMode(CustomList.SingleSelection)
        train = QListWidgetItem("Training")
        train.setTextAlignment(QtCore.Qt.AlignCenter)
        test = QListWidgetItem("Testing")
        test.setTextAlignment(QtCore.Qt.AlignCenter)
        self.list.addItem(train)
        self.list.addItem(test)
        self.list.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.list.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        shadow = QGraphicsDropShadowEffect()
        shadow.setColor(QColor(179, 179, 179, 40).darker(800))
        shadow.setXOffset(1)
        shadow.setYOffset(0)
        self.list.setGraphicsEffect(shadow)
        self.list.setCurrentRow(0)

        self.stack = QStackedLayout()
        self.stack.addWidget(TrainingWidget())
        self.stack.addWidget(TestingWidget())

        self.list.currentRowChanged.connect(self.stack.setCurrentIndex)
        box.setSpacing(70)
        box.addWidget(self.list)
        box.addLayout(self.stack)
        self.setLayout(box)


        self.setObjectName("main")
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.setWindowTitle('Demo')
        self.show()
