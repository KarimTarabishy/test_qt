import sys

from PyQt5.QtWidgets import QApplication
from gui.main_widget import MainWidget


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWidget()
    app.setStyleSheet("QWidget#main{padding: 0px; background-color:#f5f5f5;}"
                      "QListWidget{ \
                            font-size: 15 px; \
                            color: black; \
                            text-align: center; \
                            border: none; \
                            border-right: 1px solid rgb(179, 179, 179, 40); \
                            background-color: #e6e6e6; \
                            margin: 0px; padding-top:50px;\
                            outline: none;\
                      }"
                      "QListView::item{ \
                            padding: 20px;\
                            color: #404040 \
                      }"
                      "QListView::item:selected, "
                      "QListView::item:selected:!active, "
                      "QListView::item:checked,"
                      "QListView::item:hover,"
                      "QListView::item:selected:active{ \
                          background-color: rgb(216,216,216); \
                          \
                      }"
                      )
    sys.exit(app.exec_())