from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton


class TestingWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        box = QHBoxLayout()
        but = QPushButton("Testing")
        box.addWidget(but)
        self.setLayout(box)
