# -*- coding:utf-8 -*-

"""
@project: SkyDrive
@file: SkyDrive.py
@author: dangzhiteng
@email: 642212607@qq.com
@date: 2018-11-23
"""

import sys
import qdarkstyle
from resource import source_rc
from queue import Queue
from threading import Thread
from Connection import Connection
from HandleThread import HandleThread
from LoginUi import LoginUi
from ConfigureUi import ConfigureUi
from MainwindowUi import MainwindowUi 
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
from PyQt5.QtCore import QObject, QFile
from PyQt5.QtGui import QIcon

class SkyDrive(QObject):

    msg_queue = Queue()

    def __init__(self):
        super(SkyDrive, self).__init__()
        self.login_widget = LoginUi()
        self.main_window = MainwindowUi()
        self.send_thread = Connection(self.msg_queue)
        self.handle_thread = HandleThread(self.msg_queue)

        self.login_widget.login_button.clicked.connect(self.login)

        self.handle_thread.login_signal.connect(self.login_result)
        self.handle_thread.file_list_signal.connect( \
        self.main_window.my_skydrive_widget.list_file)
        self.main_window.trans_list_widget.upload_widget.reday_up_signal.connect(\
        self.send_thread.reday_up)
        self.handle_thread.port_signal.connect( \
        self.main_window.trans_list_widget.upload_widget.add_port)
        self.main_window.my_skydrive_widget.cd_folder_signal.connect(\
        self.send_thread.cd_folder)        
        self.main_window.my_skydrive_widget.delete_signal.connect(\
        self.send_thread.delete)
        self.main_window.my_skydrive_widget.refresh_signal.connect(\
        self.send_thread.cd_folder)
        self.main_window.my_skydrive_widget.rename_signal.connect(\
        self.send_thread.rename)
        self.main_window.my_skydrive_widget.mkdir_signal.connect(\
        self.send_thread.mkdir)
        self.login_widget.show()

    def login(self):
        self.send_thread.login(self.login_widget.configure.ip_line.text(), \
                               self.login_widget.configure.port_line.text(), \
                               self.login_widget.username_line.text(), \
                               self.login_widget.password_line.text())
        self.handle_thread.start()

    def login_result(self, status):
        if status:
            self.login_widget.hide()
            self.main_window.show()
        else:
            QMessageBox.warning(self, '警告', '账号或密码错误！')

    def upload_files(self, file_list, target_folder):
        self.send_thread.upload_files(file_list, target_folder)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    qss = open('./resource/myqss.qss', 'r')
    app.setStyleSheet(qss.read())
    skydrive = SkyDrive()
    sys.exit(app.exec_())