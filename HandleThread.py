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

    login_signal = pyqtSignal(bool)
    notice_sharecode_signal = pyqtSignal(str, str)
    size_signal = pyqtSignal(dict)
    file_list_signal = pyqtSignal(dict)
    port_signal = pyqtSignal(str, int)

    def __init__(self, queue):
        super(HandleThread, self).__init__()
        self.queue = queue

    def run(self):
        print('消息处理线程已启动......')
        while True:
            cur_message = self.queue.get()
            print(cur_message)
            if cur_message['CMD'] == 'LOGIN':
                self.login_signal.emit(cur_message['STATUS'])
                self.notice_sharecode_signal.emit(cur_message['NOTICE'], cur_message['SHARECODE'])
            elif cur_message['CMD'] == 'LIST':
                file_list = cur_message['FILELIST']
                other_info = cur_message['OTHERINFO']
                self.file_list_signal.emit(file_list)
                self.size_signal.emit(other_info)
            elif cur_message['CMD'] == 'REDAYUP':
                file_name = cur_message['FILENAME']
                port = cur_message['PORT']
                print('用户申请到服务器端口', port, '用来上传', file_name)
                self.port_signal.emit(file_name, port)
            elif cur_message['CMD'] == 'REDAYDOWN':
                file_name = cur_message['FILENAME']
                port = cur_message['PORT']
                print('用户申请到服务器端口', port, '用来下载', file_name)
                self.port_signal.emit(file_name, port)
        print('消息处理线程已结束......')

