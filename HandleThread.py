# -*- coding:utf-8 -*-
import json
from PyQt5.QtCore import pyqtSignal, QObject, QThread

class HandleThread(QThread):

    login_signal = pyqtSignal(bool, str)
    file_list_signal = pyqtSignal(dict)
    ports_signal = pyqtSignal(list)
    move_signal = pyqtSignal(bool)

    def __init__(self, queue):
        super(HandleThread, self).__init__()
        self.queue = queue

    def run(self):
        while True:
            cur_message = self.queue.get()
            if cur_message['CMD'] == 'LOGIN':
                self.login_signal.emit(cur_message['STATUS'], cur_message['HASHKEY'])
            elif cur_message['CMD'] == 'LIST':
                file_list = cur_message['FILELIST']
                self.file_list_signal.emit(file_list)
            elif cur_message['CMD'] == 'GETPORTS':
                ports = cur_message['PORTS']
                self.ports_signal.emit(ports)
