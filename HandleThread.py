# -*- coding:utf-8 -*-

"""
@project: SkyDrive
@file: SkyDrive.py
@author: dangzhiteng
@email: 642212607@qq.com
@date: 2018-11-23
"""

import json
from PyQt5.QtCore import pyqtSignal, QObject, QThread

class HandleThread(QThread):

    login_signal = pyqtSignal(bool, str)
    file_list_signal = pyqtSignal(dict)
    port_signal = pyqtSignal(str, int)

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
            elif cur_message['CMD'] == 'REDAYUP':
                file_name = cur_message['FILENAME']
                port = cur_message['PORT']
                print('用户申请到服务器端口', port, '用来上传', file_name)
                self.port_signal.emit(file_name, port)
