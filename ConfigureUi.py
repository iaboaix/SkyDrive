# -*- coding:utf-8 -*-

"""
@project: SkyDrive
@file: SkyDrive.py
@author: dangzhiteng
@email: 642212607@qq.com
@date: 2018-11-23
"""

from resource import source_rc
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, 
                             QGridLayout, QMessageBox, QSizePolicy)
from PyQt5.QtCore import QSettings, Qt
from PyQt5.QtGui import QIcon

class ConfigureUi(QWidget):

    def __init__(self):
        super(ConfigureUi, self).__init__()
        self.setWindowTitle('Setting')
        self.setWindowIcon(QIcon(':/default/default_icons/setting_normal.ico'))
        self.factor = self.__width__ = QApplication.desktop().screenGeometry().width()/100
        self.resize(self.factor*18, self.factor*10)
        ip_label = QLabel('IP:')
        port_label = QLabel('Port:')
        self.ip_line = QLineEdit()
        self.port_line = QLineEdit()
        self.configure_button = QPushButton('确认', clicked=self.update_setting)
        
        main_layout = QGridLayout()
        main_layout.setSpacing(self.factor/2)
        main_layout.addWidget(ip_label, 0, 0)       
        main_layout.addWidget(self.ip_line, 0, 1)       
        main_layout.addWidget(port_label, 1, 0)
        main_layout.addWidget(self.port_line, 1, 1)
        main_layout.addWidget(self.configure_button, 2, 1, Qt.AlignRight)

        self.setLayout(main_layout)

        ip_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        port_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        self.ip_line.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.port_line.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.configure_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.configure_button.setFixedWidth(self.factor*4)

        self.setting = QSettings('gfkd', 'SkyDrive')
        ip_address = self.setting.value('SkyDrive/ip_address')
        port = self.setting.value('SkyDrive/port')
        is_remember = self.setting.value('SkyDrive/is_remember')
        is_auto_login = self.setting.value('SkyDrive/is_auto_login')
        print('Default Setting:', ip_address, port)
        # 第一次登录时，初始化默认配置
        if (ip_address is None) or (port is None):
            ip_address = '139.199.163.147'
            port = '50005'
            self.setting.setValue('SkyDrive/ip_address', ip_address)
            self.setting.setValue('SkyDrive/port', port)               
            self.setting.setValue('SkyDrive/is_remember', 0)
            self.setting.setValue('SkyDrive/is_auto_login', 0)
            self.setting.setValue('SkyDrive/username', '')
            self.setting.setValue('SkyDrive/password', '')
            self.ip_line.setText(ip_address)
            self.port_line.setText(port) 
        self.ip_line.setText(ip_address)
        self.port_line.setText(port) 

    def update_setting(self):
        self.setting.setValue('SkyDrive/ip_address', self.ip_line.text())
        self.setting.setValue('SkyDrive/port', self.port_line.text())   
        QMessageBox.information(self, 'Success', '配置更新成功！')   
        self.close()  


if __name__ == '__main__':
    import sys
    import qdarkstyle
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    login = ConfigureUi()
    login.show()
    sys.exit(app.exec_())
