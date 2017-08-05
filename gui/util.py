from PyQt5.QtWidgets import QMessageBox


def showError(msg):
    box = QMessageBox()
    box.setText(msg)
    box.setStandardButtons(QMessageBox.Ok)
    box.setWindowTitle("Error")
    box.setIcon(QMessageBox.Critical)
    return box.exec_()