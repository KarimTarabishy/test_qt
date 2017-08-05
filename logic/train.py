
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from multiprocessing import Process, Queue
from .message import Message
import keras

class KerasCallback(keras.callbacks.Callback):
    def __init__(self, queue):
        super(KerasCallback, self).__init__()
        self.queue = queue

    def on_epoch_end(self, epoch, logs={}):
        print(epoch)
        print(logs)
        return



class TrainRunner(QObject):
    """
    Runs a job in a separate process and forwards messages from the job to the
    main thread through a pyqtSignal.

    """

    msg_from_job = pyqtSignal(object)

    def __init__(self, start_signal, data_dir, save_dir):
        """
        :param start_signal: the pyqtSignal that starts the job

        """
        super(TrainRunner, self).__init__()
        start_signal.connect(self._run)
        self.data_dir = data_dir
        self.save_dir = save_dir

    @pyqtSlot()
    def _run(self):
        queue = Queue()
        p = Process(target=train, args=(queue, self.data_dir, self.save_dir ))
        p.start()
        while True:
            msg = queue.get()
            self.msg_from_job.emit(msg)
            if msg.type == "command" and msg.data == "end":
                break

def train(queue, data_dir, save_dir):
    queue.put(Message("text", "Initializing..."))
    import keras
    from keras.datasets import mnist
    from keras.models import Sequential
    from keras.layers import Dense, Dropout, Flatten
    from keras.layers import Conv2D, MaxPooling2D
    from keras import backend as K

    batch_size = 128
    num_classes = 10
    epochs = 2

    # input image dimensions
    img_rows, img_cols = 28, 28

    # the data, shuffled and split between train and test sets
    (x_train, y_train), (x_test, y_test) = mnist.load_data()

    if K.image_data_format() == 'channels_first':
        x_train = x_train.reshape(x_train.shape[0], 1, img_rows, img_cols)
        x_test = x_test.reshape(x_test.shape[0], 1, img_rows, img_cols)
        input_shape = (1, img_rows, img_cols)
    else:
        x_train = x_train.reshape(x_train.shape[0], img_rows, img_cols, 1)
        x_test = x_test.reshape(x_test.shape[0], img_rows, img_cols, 1)
        input_shape = (img_rows, img_cols, 1)

    x_train = x_train.astype('float32')
    x_test = x_test.astype('float32')
    x_train /= 255
    x_test /= 255
    print('x_train shape:', x_train.shape)
    print(x_train.shape[0], 'train samples')
    print(x_test.shape[0], 'test samples')

    # convert class vectors to binary class matrices
    y_train = keras.utils.to_categorical(y_train, num_classes)
    y_test = keras.utils.to_categorical(y_test, num_classes)

    model = Sequential()
    model.add(Conv2D(32, kernel_size=(3, 3),
                     activation='relu',
                     input_shape=input_shape))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Flatten())
    model.add(Dense(num_classes, activation='softmax'))

    model.compile(loss=keras.losses.categorical_crossentropy,
                  optimizer=keras.optimizers.Adadelta(),
                  metrics=['accuracy'])
    queue.put(Message("text", "Training..."))
    model.fit(x_train, y_train,
              batch_size=batch_size,
              epochs=epochs,
              verbose=1,
              validation_data=(x_test, y_test),
              callbacks=KerasCallback(queue))
    score = model.evaluate(x_test, y_test, verbose=0)
    print('Test loss:', score[0])
    print('Test accuracy:', score[1])
    queue.put(Message("command", "end"))