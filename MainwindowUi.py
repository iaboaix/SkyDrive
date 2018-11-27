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
                              QHBoxLayout, QStackedLayout, QProgressBar)
from PyQt5.QtGui import QIcon, QPixmap, QBrush, QFont, QCursor
from PyQt5.QtCore import pyqtSignal, Qt

class MainwindowUi(QWidget):

    table_cloumn = 8
    upload_signal = pyqtSignal(list, str)
    hover_user_signal = pyqtSignal()

    def __init__(self):
        super(MainwindowUi, self).__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.factor = QApplication.desktop().screenGeometry().width()/100
        self.setWindowTitle('SkyDrive')
        self.setWindowIcon(QIcon(':/default/icons/SkyDrive.ico'))
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
        title_function_layout.addWidget(self.my_skydrive)
        title_function_layout.addWidget(self.trans_list)
        title_function_layout.addWidget(self.friend_share)

        user_info_layout = QHBoxLayout()
        user_info_layout.setSpacing(0)
        self.user_image = QLabel()
        self.user_name = QPushButton()
        self.user_is_vip = QPushButton()
        user_info_layout.addWidget(self.user_image)
        user_info_layout.addWidget(self.user_name)
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
        tools_layout.setSpacing(0)

        title_layout = QHBoxLayout()
        title_layout.setSpacing(0)
        title_layout.addWidget(self.logo_image)
        title_layout.addWidget(self.logo_name)
        title_layout.addStretch(1)
        title_layout.addLayout(title_function_layout)
        title_layout.addStretch(13)
        title_layout.addLayout(user_info_layout)
        title_layout.addStretch(1)
        title_layout.addLayout(tools_layout)
        
        self.my_skydrive_widget = QWidget(self)
        self.my_skydrive_layout = QHBoxLayout()
        self.select_type = QTableWidget(11, 1)
        self.select_type.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.select_type.horizontalHeader().setHidden(True)
        self.select_type.verticalHeader().setHidden(True) 
        self.select_type.setShowGrid(False)
        self.select_type.setFocusPolicy(Qt.NoFocus)
        items = ['最近使用', '全部文件', '\b\b\b\b图片', '\b\b\b\b视频', '\b\b\b\b文档', '\b\b\b\b音乐',\
                 '\b\b\b\b种子', '\b\b\b\b其他', '隐藏空间', '我的分享', '回收站']
        for index, item in enumerate(items):
            self.select_type.setRowHeight(index, self.factor*3)
            self.select_type.setItem(index, 0, QTableWidgetItem(item))

        select_type_layout = QVBoxLayout()
        self.capacity_bar = QProgressBar()
        # 测试
        self.capacity_bar.setValue(30)
        capacity_layout = QHBoxLayout()
        # 测试
        self.capacity_info = QLabel('30G/100G')
        self.expand_capacity = QPushButton()
        capacity_layout.addWidget(self.capacity_info)
        capacity_layout.addStretch()
        capacity_layout.addWidget(self.expand_capacity)
        select_type_layout.addStretch()
        select_type_layout.addWidget(self.capacity_bar)
        select_type_layout.addLayout(capacity_layout)
        self.select_type.setLayout(select_type_layout)

        self.file_table = QTableWidget(0, 8)
        self.file_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.file_table.horizontalHeader().setHidden(True)
        self.file_table.verticalHeader().setHidden(True)
        self.file_table.setShowGrid(False)
        self.file_table.setFocusPolicy(Qt.NoFocus)

        self.my_skydrive_layout.addWidget(self.select_type)
        self.my_skydrive_layout.addWidget(self.file_table)
        self.my_skydrive_layout.setStretchFactor(self.select_type, 1)
        self.my_skydrive_layout.setStretchFactor(self.file_table, 6)
        self.my_skydrive_widget.setLayout(self.my_skydrive_layout)

        self.trans_list_widget = QWidget(self)

        self.friend_share_widget = QWidget(self)

        self.stacked_layout = QStackedLayout()
        self.stacked_layout.addWidget(self.my_skydrive_widget)
        self.stacked_layout.addWidget(self.trans_list_widget)
        self.stacked_layout.addWidget(self.friend_share_widget)

        main_layout = QVBoxLayout()        
        main_layout.addLayout(title_layout)
        main_layout.addLayout(self.stacked_layout)

        self.setLayout(main_layout)

        self.setupUi()

        self.my_skydrive.clicked.connect(self.my_skydrive_clicked)
        self.trans_list.clicked.connect(self.trans_list_cliecked)
        self.friend_share.clicked.connect(self.friend_share_clicked)
        self.minimize_button.clicked.connect(self.showMinimized)
        self.close_button.clicked.connect(self.showMaximized)
        self.close_button.clicked.connect(self.close)
        # self.user_name.hovered.connect(self.hover_user_signal.emit)


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
        self.expand_capacity.setObjectName('link')
        self.logo_image.setPixmap(QPixmap(':/default/pngs/SkyDrive.png').\
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
        self.user_image.setPixmap(QPixmap(':/default/pngs/plush.png'))
        self.user_name.setText('admin')
        self.user_name.setFont(font)
        self.user_is_vip.setCursor(QCursor(Qt.PointingHandCursor))
        self.user_is_vip.setIcon(QIcon(':/default/icons/not_crown.ico'))
        qss = open('./resource/myqss.qss', 'r')
        self.setStyleSheet(qss.read())
        self.select_type.item(0, 0).setIcon(QIcon(':/default/icons/recent_normal.ico'))
        self.select_type.item(1, 0).setIcon(QIcon(':/default/icons/files_normal.ico'))
        self.select_type.item(8, 0).setIcon(QIcon(':/default/icons/hide_space_normal.ico'))
        self.select_type.item(9, 0).setIcon(QIcon(':/default/icons/share_normal.ico'))
        self.select_type.item(10, 0).setIcon(QIcon(':/default/icons/trash_normal.ico'))
        self.expand_capacity.setCursor(QCursor(Qt.PointingHandCursor))
        self.expand_capacity.setText('扩容')

    def my_skydrive_clicked(self):
        self.stacked_layout.setCurrentIndex(0)
        self.my_skydrive.setChecked(True)
        self.trans_list.setChecked(False)
        self.friend_share.setChecked(False)

    def trans_list_cliecked(self):
        self.stacked_layout.setCurrentIndex(1)
        self.my_skydrive.setChecked(False)
        self.trans_list.setChecked(True)
        self.friend_share.setChecked(False)

    def friend_share_clicked(self):
        self.stacked_layout.setCurrentIndex(2)
        self.my_skydrive.setChecked(False)
        self.trans_list.setChecked(False)
        self.friend_share.setChecked(True)

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
            try:
                self.move(event.globalPos() - self.dragPosition)
                event.accept()
            except:
                pass

if __name__ == '__main__':
    import sys
    import qdarkstyle
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    win = MainwindowUi()
    win.show()
    sys.exit(app.exec_())