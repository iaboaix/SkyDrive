 # -*- coding:utf-8 -*-
 # # # # # # # # # # # # # # #
 # @file   LoginUi           #
 # @email  642212607@qq.com  #
 # @date   2018-11-24        #
 # # # # # # # # # # # # # # #

import time
from MySkyDriveWidget import MySkyDriveWidget
from TransListWidget import TransListWidget
from resource import source_rc
from UserInfoUi import UserInfoUi
from PyQt5.QtWidgets import  (QApplication, QWidget, QLabel, QPushButton, 
                              QVBoxLayout, QHeaderView, QHBoxLayout, 
                              QStackedWidget, QProgressBar, QListWidget, QListWidgetItem,
                              QButtonGroup)
from PyQt5.QtGui import QIcon, QPixmap, QBrush, QFont, QCursor, QDrag
from PyQt5.QtCore import pyqtSignal, Qt, QMimeData, QRect, QSize, QPoint, QTimer

class MainwindowUi(QWidget):

    table_cloumn = 8
    hover_user_signal = pyqtSignal()

    def __init__(self):
        super(MainwindowUi, self).__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.factor = QApplication.desktop().screenGeometry().width()/100
        self.setWindowTitle('SkyDrive')
        self.setWindowIcon(QIcon(':/default/default_icons/SkyDrive.ico'))
        self.resize(self.factor*80, self.factor*50)

        self.logo_image = QLabel()
        self.logo_name = QLabel()
        title_function_layout = QHBoxLayout()
        title_function_layout.setSpacing(self.factor)
        self.my_skydrive = QPushButton()
        self.my_skydrive.setCheckable(True)
        self.my_skydrive.setChecked(True)
        self.trans_list = QPushButton()
        self.trans_list.setCheckable(True)
        self.friend_share = QPushButton()
        self.friend_share.setCheckable(True)
        self.button_group = QButtonGroup()
        self.button_group.addButton(self.my_skydrive, 0)
        self.button_group.addButton(self.trans_list, 1)
        self.button_group.addButton(self.friend_share, 2)
        title_function_layout.addWidget(self.my_skydrive)
        title_function_layout.addWidget(self.trans_list)
        title_function_layout.addWidget(self.friend_share)

        user_info_layout = QHBoxLayout()
        user_info_layout.setSpacing(0)
        self.user_image = QLabel()
        self.user_name = SignalPushButton()
        self.user_is_vip = QPushButton()
        user_info_layout.addWidget(self.user_image)
        user_info_layout.addWidget(self.user_name)
        user_info_layout.addWidget(self.user_is_vip)

        tools_layout = QHBoxLayout()
        self.setting_button = QPushButton()
        self.minimize_button = QPushButton(clicked=self.showMinimized)
        self.maximize_button = QPushButton(clicked=self.showMaximized)
        self.close_button = QPushButton(clicked=self.close)
        self.setting_button.setObjectName('setting_button')
        self.minimize_button.setObjectName('minimize_button')
        self.maximize_button.setObjectName('maximize_button')
        self.close_button.setObjectName('close_button')

        tools_layout.addWidget(self.setting_button)
        tools_layout.addWidget(self.minimize_button)
        tools_layout.addWidget(self.maximize_button)
        tools_layout.addWidget(self.close_button)
        tools_layout.setSpacing(0)

        title_layout = QHBoxLayout()
        title_layout.setSpacing(0)
        title_layout.addWidget(self.logo_image)
        title_layout.addWidget(self.logo_name)
        title_layout.addStretch(2)
        title_layout.addLayout(title_function_layout)
        title_layout.addStretch(12)
        title_layout.addLayout(user_info_layout)
        title_layout.addStretch(1)
        title_layout.addLayout(tools_layout)
        
        stacked_layout = QStackedWidget()
        self.my_skydrive_widget = MySkyDriveWidget()
        self.trans_list_widget = TransListWidget()
        self.friend_share_widget = QWidget(self)
        stacked_layout.addWidget(self.my_skydrive_widget)
        stacked_layout.addWidget(self.trans_list_widget)
        stacked_layout.addWidget(self.friend_share_widget)

        main_layout = QVBoxLayout()        
        main_layout.addLayout(title_layout)
        main_layout.addWidget(stacked_layout)
        self.setLayout(main_layout)
        self.setupUi()

        self.user_info_widget = UserInfoUi()

        self.button_group.buttonClicked[int].connect(stacked_layout.setCurrentIndex)
        self.user_name.enter_signal.connect(self.mouseEnter)
        self.user_name.leave_signal.connect(self.mouseLeave)
        self.user_info_widget.enter_signal.connect(self.mouseEnter)
        self.user_info_widget.leave_signal.connect(self.mouseLeave)
        self.my_skydrive_widget.file_widget.upload_signal.connect(\
        self.trans_list_widget.upload_widget.add_items)

        qss = open('./resource/myqss.qss', 'r')
        self.setStyleSheet(qss.read())

    def setupUi(self):
        self.logo_image.setCursor(QCursor(Qt.PointingHandCursor))
        self.logo_name.setCursor(QCursor(Qt.PointingHandCursor))
        self.my_skydrive.setObjectName('title_menu')
        self.trans_list.setObjectName('title_menu')
        self.friend_share.setObjectName('title_menu')
        self.my_skydrive.setFixedHeight(self.factor*3)
        self.trans_list.setFixedHeight(self.factor*3)
        self.friend_share.setFixedHeight(self.factor*3)
        self.user_name.setObjectName('transparent')
        self.user_is_vip.setObjectName('transparent')
        self.logo_image.setPixmap(QPixmap(':/default/default_pngs/SkyDrive.png').\
                  scaled(self.factor*3, self.factor*3))
        font = QFont()
        font.setPixelSize(self.factor*1.5)
        self.logo_name.setText('SkyDrive')
        self.logo_name.setFont(font)
        font.setPixelSize(self.factor*1.3)
        self.my_skydrive.setText('我的网盘')
        self.trans_list.setText('传输列表')
        self.friend_share.setText('好友分享')        
        self.my_skydrive.setFont(font)
        self.trans_list.setFont(font)
        self.friend_share.setFont(font)
        self.user_image.setPixmap(QPixmap(':/default/default_pngs/plush.png'))
        self.user_name.setText('admin')
        self.user_name.setFont(font)
        self.user_is_vip.setCursor(QCursor(Qt.PointingHandCursor))
        self.user_is_vip.setIcon(QIcon(':/default/default_icons/not_crown.ico'))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            try:
                self.move(event.globalPos() - self.dragPosition)
                event.accept()
            except:
                pass

    def mouseEnter(self, id):
        if id == 0:
            self.check = 0
            self.user_info_widget.move(self.geometry().x()+self.factor*59.5, self.geometry().y()+self.factor*3.5)
            self.user_info_widget.show()
        else:
            self.check = 1
    
    def mouseLeave(self, id):
        if id == 0:
            if self.check == 0:
                self.user_info_widget.hide()
        else:
            self.user_info_widget.hide()



class SignalPushButton(QPushButton):
  
    enter_signal = pyqtSignal(int)
    leave_signal = pyqtSignal(int)
  
    def __init__(self):
        super(SignalPushButton, self).__init__()

    def enterEvent(self, event):
        self.enter_signal.emit(0)

    def leaveEvent(self, event):
        QTimer.singleShot(500, self.emit_signal)

    def emit_signal(self):
        self.leave_signal.emit(0)

if __name__ == '__main__':
    import sys
    import qdarkstyle
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    win = MainwindowUi()
    win.show()
    sys.exit(app.exec_())