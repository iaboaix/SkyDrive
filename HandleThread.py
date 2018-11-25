# -*- coding:utf-8 -*-
import json
from PyQt5.QtCore import pyqtSignal, QObject, QThread

class HandleThread(QThread):

    login_signal = pyqtSignal(bool, str)
    list_signal = pyqtSignal(bool)
    delete_signal = pyqtSignal(bool)
    move_signal = pyqtSignal(bool)

    def __init__(self, queue):
        super(HandleThread, self).__init__()
        self.queue = queue

    def run(self):
        while True:
            cur_message = self.queue.get()
            if cur_message['CMD'] == 'LOGIN':
                self.login_signal.emit(cur_message['STATUS'], cur_message['HASHKEY'])