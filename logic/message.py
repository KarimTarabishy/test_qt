class Message(object):
    def __init__(self, type, data):
        super(Message, self).__init__()
        self.type = type
        self.data = data
