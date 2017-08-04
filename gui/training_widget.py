from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout


class TrainingWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        box = QHBoxLayout()
        but = QPushButton("Training")
        box.addWidget(but)
        self.setLayout(box)


