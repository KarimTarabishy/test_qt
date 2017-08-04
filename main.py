import sys

from PyQt5.QtWidgets import QApplication
from gui.main_widget import MainWidget


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWidget()
    app.setStyleSheet("QWidget#main{padding: 0px; background-color:rgb(255,255,255);}"
                      "QListWidget{ \
                            font-size: 20 px; \
                            color: black; \
                            text-align: center; \
                            border: none; \
                            border-right: 1px solid grey; \
                            background-color: gray; \
                            margin: 0px; \
                      }"
                      "QListView::item{ \
                            margin-bottom:20px; \
                            padding-top: 20 px; \
                            border-bottom: 1px solid gray \
                      }"


                      )
    sys.exit(app.exec_())