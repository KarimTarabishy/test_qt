from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QFileDialog, QSizePolicy, QTextEdit, \
    QProgressBar
from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal, Qt, QThread
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import os
from .util import showError
from logic.train import TrainRunner
import weakref

class TrainingWidget(QWidget):
    data_dir_selected = pyqtSignal(str)
    save_dir_selected = pyqtSignal(str)
    test_count = pyqtSignal(str)
    train_count = pyqtSignal(str)
    training = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.data_dir = None
        self.save_dir = None
        self.train_button = None
        self.text_edit = None
        self.is_training = False
        self.runner_thread = None
        self.worker = None
        self.training_info_box = {}
        self.init_ui()


    def init_ui(self):
        vbox = QVBoxLayout()
        size = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        ## Data Box
        data_hbox = QHBoxLayout()
        data_label = QLabel("Data directory: ")
        data_label.setSizePolicy(size)
        data_label_dir = QLabel("")
        data_label_dir.setSizePolicy(size)
        self.data_dir_selected.connect(data_label_dir.setText)

        data_button = QPushButton("Choose Folder")
        data_button.setSizePolicy(size)
        data_button.pressed.connect(self.data_button_pressed)

        data_hbox.addWidget(data_label)
        data_hbox.addWidget(data_label_dir)
        data_hbox.addStretch(1)
        data_hbox.addWidget(data_button)
        data_hbox.addStretch(2)

        # train box
        train_hbox = QHBoxLayout()

        train_count_label = QLabel("Training images: ")
        train_count_label.setSizePolicy(size)

        train_count_value_label = QLabel("");
        train_count_value_label.setSizePolicy(size)
        self.train_count.connect(train_count_value_label.setText)

        train_hbox.addWidget(train_count_label)
        train_hbox.addWidget(train_count_value_label)
        train_hbox.addStretch(1)

        # test box
        test_hbox = QHBoxLayout()
        test_count_label = QLabel("Testing images: ")
        test_count_value_label = QLabel("");
        test_count_label.setSizePolicy(size)
        test_count_value_label.setSizePolicy(size)
        self.test_count.connect(test_count_value_label.setText)
        test_hbox.addWidget(test_count_label)
        test_hbox.addWidget(test_count_value_label)
        test_hbox.addStretch(1)

        ## Save box
        save_hbox = QHBoxLayout()
        save_label = QLabel("Save directory: ")
        save_label.setSizePolicy(size)
        save_label_dir = QLabel("")
        save_label_dir.setSizePolicy(size)
        self.save_dir_selected.connect(save_label_dir.setText)

        save_button = QPushButton("Choose Folder")
        save_button.setSizePolicy(size)
        save_button.pressed.connect(self.save_button_pressed)

        save_hbox.addWidget(save_label)
        save_hbox.addWidget(save_label_dir)
        save_hbox.addStretch(1)
        save_hbox.addWidget(save_button)
        save_hbox.addStretch(2)

        ## Train button
        self.train_button = QPushButton("Strat Training")
        self.train_button.setMaximumWidth(300)
        self.train_button.setEnabled(False)
        self.train_button.pressed.connect(self.start_training)
        self.training.connect(self.train_button.setDisabled)


        train_info_layout = self.create_training_info()

        vbox.setSpacing(20)
        vbox.addLayout(data_hbox)
        vbox.addLayout(train_hbox)
        vbox.addLayout(test_hbox)
        vbox.addLayout(save_hbox)
        vbox.addSpacing(40)
        vbox.addWidget(self.train_button)
        vbox.addLayout(train_info_layout)
        vbox.addStretch(1)
        self.setLayout(vbox)

        self.setSizePolicy(size)
        self.setObjectName("training")


    def set_training_visible(self, visible):
        self.training_info_box["text_edit_label"].setVisible(visible)
        self.training_info_box["text_edit"].setVisible(visible)
        self.training_info_box["bar"].setVisible(visible)
        self.training_info_box["figure"].set_visible(visible)
        plt.draw()

    def create_training_info(self):
        self.training_info_box["layout"] = QVBoxLayout()

        size = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        ##QTextEdit
        self.training_info_box["text_edit_label"] = QLabel("Info: ")
        self.training_info_box["text_edit_label"].setSizePolicy(size)
        self.training_info_box["text_edit"] = QTextEdit()
        self.training_info_box["text_edit"].setFixedHeight(100)
        self.training_info_box["text_edit"].setReadOnly(True)

        ## Progress bar
        self.training_info_box["bar"] = QProgressBar()

        ## matplotlib
        self.training_info_box["figure"] = plt.figure()
        self.training_info_box["canvas"] = FigureCanvas(self.training_info_box["figure"])

        self.training_info_box["layout"].addWidget(self.training_info_box["text_edit_label"])
        self.training_info_box["layout"].addWidget(self.training_info_box["text_edit"])
        self.training_info_box["layout"].addWidget(self.training_info_box["bar"])
        self.training_info_box["layout"].addWidget(self.training_info_box["canvas"])
        self.set_training_visible(False)
        return self.training_info_box["layout"]



    def change_train_button_state(self):
        try:
            if self.data_dir is not None and self.save_dir is not None:
                self.train_button.setEnabled(True)
            else:
                self.train_button.setEnabled(False)
        except Exception as a:
            print(a)

    @pyqtSlot()
    def start_training(self):
        self.training.emit(True)
        self.runner_thread = QThread()
        self.worker = TrainRunner(self.data_dir, self.save_dir)
        self.worker.moveToThread(self.runner_thread)
        self.worker.msg_from_job.connect(self.handleRunner)
        self.runner_thread.started.connect(self.worker.run)
        self.runner_thread.start()


    @pyqtSlot(object)
    def handleRunner(self, obj):
        if obj.type == "command" and obj.data == "end":
            self.text_edit.append("Done.\n")
            self.runner_thread.quit()
            self.training.emit(False)

        elif obj.type == "total_epochs":
            self.set_training_visible(True)
            axis = self.training_info_box["figure"].gca()
            axis.y_limit([0,1])
            axis.x_limit([0, obj.data])
            self.training_info_box["bar"].setMinimum(0)
            self.training_info_box["bar"].setMaximum(obj.data)


        elif obj.type == "epoch_logs":
            self.text_edit.append("accuracy: " + str(obj.data["acc"]) + ", validation_accuracy: " +
                                  str(obj.data["val_acc"]))
        elif obj.type == "text":
            self.text_edit.append(obj.data + "\n")

    @pyqtSlot()
    def data_button_pressed(self):
        data_dir = QFileDialog.getExistingDirectory(self, "Choose data folder")
        if len(data_dir):
            try:
                if not os.path.isdir(os.path.join(data_dir, "training")) or \
                            not os.path.isdir(os.path.join(data_dir, "validation")):
                    raise Exception

                len_train = 0
                for root, dir, files in os.walk(os.path.join(data_dir, "training")):
                    len_train += len(files)

                len_test = 0
                for root, dir, files in os.walk(os.path.join(data_dir, "validation")):
                    len_test += len(files)

                self.data_dir = data_dir
                self.data_dir_selected.emit(data_dir)
                self.test_count.emit(str(len_test))
                self.train_count.emit(str(len_train))
            except Exception as e:
                print(e)
                showError("Directory doesn't have the correct structure.")
                self.data_dir_selected.emit("")
                self.test_count.emit("")
                self.train_count.emit("")
                self.data_dir = None
            finally:
                self.change_train_button_state()

    @pyqtSlot()
    def save_button_pressed(self):
        save_dir = QFileDialog.getExistingDirectory(self, "Choose save folder")
        if len(save_dir):
            self.save_dir = save_dir
            self.save_dir_selected.emit(save_dir)
            self.change_train_button_state()
