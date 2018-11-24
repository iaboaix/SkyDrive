from PyQt5.QtCore import pyqtSignal, QObject, QThread

class HandleThread(QThread):

    def __init__(self, queue):
        super(HandleThread, self).__init__()
        self.queue = queue

    def run(self):
        print(self.queue.get())
