from PyQt5.QtCore import pyqtSlot
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
        self.train_item = None
        self.test_item = None
        self.training_widget = None
        self.testing_widget = None
        self.init_ui()

    def init_ui(self):
        box = QHBoxLayout()

        self.list = CustomList()
        self.list.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.list.setSelectionMode(CustomList.SingleSelection)
        self.train_item = QListWidgetItem("Training")
        self.train_item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.test_item = QListWidgetItem("Testing")
        self.test_item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.list.addItem(self.train_item)
        self.list.addItem(self.test_item)
        self.list.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.list.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        shadow = QGraphicsDropShadowEffect()
        shadow.setColor(QColor(179, 179, 179, 40).darker(800))
        shadow.setXOffset(1)
        shadow.setYOffset(0)
        self.list.setGraphicsEffect(shadow)
        self.list.setCurrentRow(0)

        self.stack = QStackedLayout()
        self.training_widget = TrainingWidget()
        self.training_widget.training.connect(self.handle_training)
        self.testing_widget = TestingWidget()
        self.stack.addWidget(self.training_widget)
        self.stack.addWidget(self.testing_widget)

        self.list.currentRowChanged.connect(self.stack.setCurrentIndex)
        box.setSpacing(70)
        box.addWidget(self.list)
        box.addLayout(self.stack)
        self.setLayout(box)

        self.setObjectName("main")
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setWindowFlags(QtCore.Qt.Widget | QtCore.Qt.MSWindowsFixedSizeDialogHint)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.setWindowTitle('Demo')
        self.show()

    @pyqtSlot(bool)
    def handle_training(self, is_running):
        if is_running:
            self.test_item.setFlags(self.test_item.flags() & ~QtCore.Qt.ItemIsEnabled)
        else:
            self.test_item.setFlags(self.test_item.flags() | QtCore.Qt.ItemIsEnabled)