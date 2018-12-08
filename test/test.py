# -*- coding:utf-8 -*-

"""
@project: SkyDrive
@file: SkyDrive.py
@author: dangzhiteng
@email: 642212607@qq.com
@date: 2018-11-23
"""

from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, 
                             QGridLayout, QMessageBox, QSizePolicy, QHBoxLayout,
                             QListWidget, QListWidgetItem, QVBoxLayout)
from PyQt5.QtCore import QSettings, Qt
from PyQt5.QtGui import QIcon

class ConfigureUi(QWidget):

    def __init__(self):
        super(ConfigureUi, self).__init__()
        self.setWindowTitle('Setting')
        self.setWindowIcon(QIcon(':/default/default_icons/setting_normal.ico'))
        self.factor = self.__width__ = QApplication.desktop().screenGeometry().width()/100
        # self.resize(self.factor*18, self.factor*10)
        ip_label = QLabel('IP:')
        port_label = QLabel('Port:')
        self.ip_line = QLineEdit('新建文件夹')
        self.ip_line.selectAll()
        self.ip_line.setStyleSheet('border: none')
        self.port_line = QLineEdit()
        self.configure_button = QPushButton('确认')
        test_layout = QHBoxLayout()
        main_layout = QGridLayout()
        main_layout.setSpacing(self.factor/2)
        main_layout.addWidget(ip_label, 0, 0)       
        main_layout.addWidget(self.ip_line, 0, 1)       
        main_layout.addWidget(port_label, 1, 0)
        main_layout.addWidget(self.port_line, 1, 1)
        main_layout.addWidget(self.configure_button, 2, 1, Qt.AlignRight)
        self.listWidget = QListWidget()
        self.listWidget.setDragEnabled(True)
        self.listWidget.setDragDropMode(QListWidget.DragOnly)
        self.listWidget.setDefaultDropAction(Qt.IgnoreAction)
        test_layout.addLayout(main_layout)
        test_layout.addWidget(self.listWidget)
        self.setLayout(test_layout)

        # 不可行！！！
        list_layout = QVBoxLayout()
        list_layout.addWidget(QPushButton())
        list_layout.addStretch()
        self.listWidget.setLayout(list_layout)
        self.make_items()

    def make_items(self):
        for i in range(10):
            item = QListWidgetItem(str(i))
            self.listWidget.addItem(item)


if __name__ == '__main__':
    import sys
    import qdarkstyle
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    login = ConfigureUi()
    login.show()
    sys.exit(app.exec_())
