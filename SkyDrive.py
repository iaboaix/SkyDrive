 # -*- coding:utf-8 -*-
 # # # # # # # # # # # # # # #
 # @file   LoginUi           #
 # @email  642212607@qq.com  #
 # @date   2018-11-24        #
 # # # # # # # # # # # # # # #


import sys
import qdarkstyle
from resource import source_rc
from queue import Queue
from threading import Thread
from SendThread import SendThread
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
        self.LoginUi = LoginUi()
        self.ConfigureUi = ConfigureUi()
        self.MainwindowUi = MainwindowUi()
        self.SendThread = SendThread(self.msg_queue)
        self.HandleThread = HandleThread(self.msg_queue)

        self.LoginUi.setting_button.clicked.connect(self.ConfigureUi.show)
        self.LoginUi.login_button.clicked.connect(self.login)

        self.MainwindowUi.upload_signal.connect(self.upload_files)

        self.HandleThread.login_signal.connect(self.login_result)
        # self.HandleThread.

    def login(self):
        self.SendThread.login(self.ConfigureUi.ip_line.text(), \
                                  self.ConfigureUi.port_line.text(), \
                                  self.LoginUi.username_line.text(), \
                                  self.LoginUi.password_line.text())
        self.HandleThread.start()

    def login_result(self, status, hash_key):
        print('hash_key:', hash_key)
        if status:
            self.hash_key = hash_key
            self.LoginUi.hide()
            self.MainwindowUi.show()
        else:
            QMessageBox.warning(self, '警告', '账号或密码错误！')

    def upload_files(self, file_list):
        self.SendThread.upload_files(file_list)

    def show(self):
        self.LoginUi.show()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    skydrive = SkyDrive()
    skydrive.show()
    sys.exit(app.exec_())