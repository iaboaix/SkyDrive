 # -*- coding:utf-8 -*-
 # # # # # # # # # # # # # # #
 # @file   LoginUi           #
 # @email  642212607@qq.com  #
 # @date   2018-11-24        #
 # # # # # # # # # # # # # # #

from resource import source_rc
from FileItem import FileItem
from PyQt5.QtWidgets import  (QApplication, QWidget, QLabel, QPushButton, \
                              QTableWidget, QVBoxLayout, QHeaderView, QTableWidgetItem, \
                              QHBoxLayout, QStackedLayout)
from PyQt5.QtGui import QIcon, QPixmap, QBrush
from PyQt5.QtCore import pyqtSignal, Qt

class MainwindowUi(QWidget):

    table_cloumn = 8
    upload_signal = pyqtSignal(list, str)

    def __init__(self):
        super(MainwindowUi, self).__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.factor = QApplication.desktop().screenGeometry().width()/100
        self.setWindowTitle('SkyDrive')
        self.setWindowIcon(QIcon(':icons/SkyDrive.ico'))
        self.resize(self.factor*80, self.factor*50)
        
        self.logo = QLabel()
        title_function_layout = QHBoxLayout()
        self.my_skydrive = QPushButton()
        self.trans_list = QPushButton()
        self.friend_share = QPushButton()
        title_function_layout.addWidget(self.my_skydrive)
        title_function_layout.addWidget(self.trans_list)
        title_function_layout.addWidget(self.friend_share)

        user_info_layout = QHBoxLayout()
        self.user_info = QPushButton()
        self.user_is_vip = QPushButton()
        user_info_layout.addWidget(self.user_info)
        user_info_layout.addWidget(self.user_is_vip)

        tools_layout = QHBoxLayout()
        self.setting_button = QPushButton()
        self.minimize_button = QPushButton()
        self.maximize_button = QPushButton()
        self.close_button = QPushButton()
        self.setting_button.setObjectName('setting_button')
        self.minimize_button.setObjectName('minimize_button')
        self.maximize_button.setObjectName('maximize_button')
        self.close_button.setObjectName('close_button')
        tools_layout.addWidget(self.setting_button)
        tools_layout.addWidget(self.minimize_button)
        tools_layout.addWidget(self.maximize_button)
        tools_layout.addWidget(self.close_button)

        title_layout = QHBoxLayout()
        title_layout.addWidget(self.logo)
        title_layout.addLayout(title_function_layout)
        title_layout.addLayout(user_info_layout)
        title_layout.addStretch()
        title_layout.addLayout(tools_layout)
        
        self.my_skydrive_widget = QWidget()
        self.my_skydrive_layout = QHBoxLayout()
        self.select_type = QTableWidget(11, 1)
        self.select_type.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.select_type.horizontalHeader().setHidden(True)
        self.select_type.verticalHeader().setHidden(True) 
        items = ['最近使用', '全部文件', '图片', '视频', '文档', '音乐',\
                 '种子', '其他', '隐藏空间', '我的分享', '回收站']
        for index, item in enumerate(items):
            self.select_type.setItem(index, 0, QTableWidgetItem(item))
        self.file_table = QTableWidget(0, 8)
        self.file_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.file_table.horizontalHeader().setHidden(True)
        self.file_table.verticalHeader().setHidden(True)        
        self.my_skydrive_layout.addWidget(self.select_type)
        self.my_skydrive_layout.addWidget(self.file_table)
        self.my_skydrive_layout.setStretchFactor(self.select_type, 1)
        self.my_skydrive_layout.setStretchFactor(self.file_table, 6)
        self.my_skydrive_widget.setLayout(self.my_skydrive_layout)

        self.stacked_layout = QStackedLayout()
        self.stacked_layout.addWidget(self.my_skydrive_widget)

        main_layout = QVBoxLayout()        
        main_layout.addLayout(title_layout)
        main_layout.addLayout(self.stacked_layout)

        self.setLayout(main_layout)

        self.setupUi()

        self.minimize_button.clicked.connect(self.showMinimized)
        self.close_button.clicked.connect(self.showMaximized)
        self.close_button.clicked.connect(self.close)

    def setupUi(self):
        self.logo.setPixmap(QPixmap(':/pngs/skydrive.png'))
        self.my_skydrive.setText('我的网盘')
        self.trans_list.setText('传输列表')
        self.trans_list.setText('好友分享')
        qss = open('./resource/myqss.qss', 'r')
        self.setStyleSheet(qss.read())

    def my_skydrive_clicked(self):
        pass

    def list_file(self, file_list):
        file_count = len(file_list)
        self.file_table.setRowCount(int(file_count/self.table_cloumn + 1))
        row = 0
        col = 0
        for file in file_list.keys():
            print(file, file_list[file][0])
            item = FileItem(file, file_list[file][0])
            item.upload_signal.connect(self.upload_signal)
            self.file_table.setCellWidget(row, col, item)
            self.file_table.setRowHeight(row, 200)
            col += 1
            if col > 7:
                row += 1
                col = 0

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
    win = MainwindowUi()
    win.show()
    sys.exit(app.exec_())