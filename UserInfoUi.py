# -*- coding:utf-8 -*-

"""
@project: SkyDrive
@file: SkyDrive.py
@author: dangzhiteng
@email: 642212607@qq.com
@date: 2018-11-23
"""

from resource import source_rc
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel,
                             QHBoxLayout, QVBoxLayout, QListWidget, QProgressBar,
                             QHeaderView, QListWidgetItem, QSizePolicy)
from PyQt5.QtGui import QPixmap, QIcon, QBrush, QCursor, QPainter, QColor
from PyQt5.QtCore import Qt, QSize, pyqtSignal, QTimer


class UserInfoUi(QWidget):

    enter_signal = pyqtSignal(int)
    leave_signal = pyqtSignal(int)

    def __init__(self):
        super(UserInfoUi, self).__init__()
        self.factor = QApplication.desktop().screenGeometry().width()/100
        self.resize(self.factor*16, self.factor*20)
        self.setWindowOpacity(1)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True);
        self.setContentsMargins(0, 0, 0, 0)
        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        v_layout = QVBoxLayout()
        h_layout = QHBoxLayout()
        self.user_name = QPushButton('admin')
        self.is_vip = QPushButton()
        self.is_vip.setCursor(QCursor(Qt.PointingHandCursor))
        self.is_vip.setIcon(QIcon(':/default/default_icons/is_crown.ico'))
        h_layout.addWidget(self.user_name)
        h_layout.addWidget(self.is_vip)
        h_layout.addStretch()
        self.capacity_bar = QProgressBar()
        self.capacity_bar.setFixedHeight(20)
        self.capacity_bar.setTextVisible(False)
        self.capacity_bar.setValue(30)
        self.capacity_info = QLabel('30G/100G')
        v_layout.addLayout(h_layout)
        v_layout.addWidget(self.capacity_bar)
        v_layout.addWidget(self.capacity_info)
        self.v_widget = QWidget(self)
        self.v_widget.setWindowOpacity(1)
        self.v_widget.setLayout(v_layout)
        self.personal_center = QPushButton('个人中心')
        self.help_center = QPushButton('帮助中心')
        self.switch_account = QPushButton('切换账号')
        self.exit_account = QPushButton('退出')
        self.personal_center.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.help_center.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.switch_account.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.exit_account.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        button_widget = QWidget()
        button_layout = QVBoxLayout()
        button_layout.setSpacing(self.factor*0.5)
        button_layout.addWidget(self.personal_center)
        button_layout.addWidget(self.help_center)
        button_layout.addWidget(self.switch_account)
        button_layout.addWidget(self.exit_account)
        button_widget.setLayout(button_layout)
        main_layout.addWidget(self.v_widget)
        main_layout.addWidget(button_widget)
        main_layout.setStretchFactor(self.v_widget, 2)
        main_layout.setStretchFactor(button_widget, 10)
        self.setLayout(main_layout)

        self.v_widget.setObjectName('user_info')
        self.user_name.setObjectName('transparent')
        self.is_vip.setObjectName('transparent')
        self.capacity_info.setObjectName('transparent')
        button_widget.setObjectName('color')

    def enterEvent(self, event):
        self.enter_signal.emit(1)

    def leaveEvent(self, event):
        QTimer.singleShot(500, self.emit_signal)

    def emit_signal(self):
        self.leave_signal.emit(1)
        

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    win = UserInfoUi()
    win.show()
    sys.exit(app.exec_())


