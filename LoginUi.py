# -*- coding:utf-8 -*-

"""
@project: SkyDrive
@file: SkyDrive.py
@author: dangzhiteng
@email: 642212607@qq.com
@date: 2018-11-23
"""

import time
from threading import Thread
from ConfigureUi import ConfigureUi
from resource import source_rc
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QGridLayout, QLineEdit,
                             QCheckBox, QVBoxLayout, QHBoxLayout, QSizePolicy)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import pyqtSignal, Qt, QObject, QSettings

class LoginUi(QWidget):

    def __init__(self):
        super(LoginUi, self).__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowTitle('SkyDrive')
        self.setWindowIcon(QIcon(':/default/default_icons/SkyDrive.ico'))
        self.factor = QApplication.desktop().screenGeometry().width()/100
        self.resize(self.factor*25, self.factor*40)
        
        self.configure = ConfigureUi()

        self.setting_button = QPushButton(clicked=self.configure.show)
        self.minimize_button = QPushButton(clicked=self.showMinimized)
        self.close_button = QPushButton(clicked=self.close)
        self.logo = QLabel()
        self.user_logo = QLabel()
        self.password_logo = QLabel()
        self.username_line = QLineEdit()
        self.password_line = QLineEdit()
        self.username_line.setPlaceholderText('username')
        self.password_line.setPlaceholderText('password')
        self.password_line.setEchoMode(QLineEdit.Password)

        self.register_button = QPushButton()
        self.find_password_button = QPushButton()
        self.is_remember_checkbox = QCheckBox(stateChanged=self.set_remember)
        self.is_autologin_checkbox = QCheckBox(stateChanged=self.set_autologin)
        self.login_button = QPushButton(clicked=self.save_pass)
        self.login_button.setObjectName('login')

        self.logo.setAlignment(Qt.AlignHCenter)
        self.username_line.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.password_line.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.login_button.setFixedHeight(self.factor*5)
        
        tools_layout = QHBoxLayout()
        tools_layout.setSpacing(0)
        tools_layout.addWidget(self.setting_button)
        tools_layout.addWidget(self.minimize_button)
        tools_layout.addWidget(self.close_button)
        tools_layout.setAlignment(Qt.AlignRight)

        user_layout = QHBoxLayout()
        user_layout.addWidget(self.user_logo)
        user_layout.addWidget(self.username_line)
        user_layout.addWidget(self.register_button)     
        
        password_layout = QHBoxLayout()
        password_layout.addWidget(self.password_logo)
        password_layout.addWidget(self.password_line)
        password_layout.addWidget(self.find_password_button)
        checkbox_layout = QHBoxLayout()
        checkbox_layout.addWidget(self.is_remember_checkbox)
        checkbox_layout.addWidget(self.is_autologin_checkbox)
        
        v_layout = QVBoxLayout()
        v_layout.addLayout(user_layout)
        v_layout.addLayout(password_layout)
        v_layout.addStretch(1)
        v_layout.addLayout(checkbox_layout)
        v_layout.setContentsMargins(self.factor*3, self.factor*2, self.factor*3, self.factor)
        
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.login_button)
        h_layout.setContentsMargins(self.factor, self.factor, self.factor, self.factor)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, self.factor*3)        
        main_layout.addLayout(tools_layout)
        main_layout.addWidget(self.logo)
        main_layout.addLayout(v_layout)
        main_layout.addLayout(h_layout)

        self.setLayout(main_layout)
        self.setupUi()

        self.setting = QSettings('gfkd', 'SkyDrive')
        username = self.setting.value('SkyDrive/username')
        password = self.setting.value('SkyDrive/password')
        is_remember = self.setting.value('SkyDrive/is_remember')
        is_auto_login = self.setting.value('SkyDrive/is_auto_login')
        self.username_line.setText(username)
        self.password_line.setText(password)
        self.is_remember_checkbox.setCheckState(is_remember)
        self.is_autologin_checkbox.setCheckState(is_auto_login)
        thread = Thread(target=self.auto_login)
        thread.start()

    def setupUi(self):
        self.is_remember_checkbox.setText('记住密码')
        self.is_autologin_checkbox.setText('自动登录')
        self.login_button.setText('登录')
        self.logo.setPixmap(QPixmap(':/default/default_pngs/SkyDrive.png'). \
                            scaled(self.factor*16, self.factor*16))
        self.user_logo.setPixmap(QPixmap(':/default/default_pngs/user_normal.png'). \
                            scaled(self.factor*2, self.factor*2))
        self.password_logo.setPixmap(QPixmap(':/default/default_pngs/password_normal.png'). \
                            scaled(self.factor*2, self.factor*2))
        self.setting_button.setObjectName('setting_button')
        self.minimize_button.setObjectName('minimize_button')
        self.close_button.setObjectName('close_button')

    def set_remember(self, state):
        self.setting.setValue('SkyDrive/is_remember', state)

    def set_autologin(self, state):
        self.setting.setValue('SkyDrive/is_auto_login', state)
        if state == 2:
            self.setting.setValue('SkyDrive/is_remember', 2)
            self.is_remember_checkbox.setCheckState(2)

    def auto_login(self):
        if self.setting.value('SkyDrive/is_auto_login') == 2:
            time.sleep(0.5)
            self.login_button.click()

    def save_pass(self):
        if self.is_remember_checkbox.checkState() == 2:
            self.setting.setValue('SkyDrive/username', self.username_line.text())
            self.setting.setValue('SkyDrive/password', self.password_line.text())
        else:
            self.setting.setValue('SkyDrive/username', '')
            self.setting.setValue('SkyDrive/password', '')

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.dragPosition)
            event.accept()



if __name__ == '__main__':
    import sys
    import qdarkstyle
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    login = LoginUi()
    login.setupUi()
    login.show()
    sys.exit(app.exec_())
