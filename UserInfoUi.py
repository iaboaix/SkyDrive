from resource import source_rc
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel,
                             QHBoxLayout, QVBoxLayout, QListWidget, QProgressBar,
                             QHeaderView, QListWidgetItem)
from PyQt5.QtGui import QPixmap, QIcon, QBrush, QCursor
from PyQt5.QtCore import Qt, QSize
class UserInfoUi(QWidget):
    def __init__(self):
        super(UserInfoUi, self).__init__()
        self.factor = QApplication.desktop().screenGeometry().width()/100
        self.resize(self.factor*16, self.factor*20)
        self.setWindowOpacity(1)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
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
        self.list_widget = QListWidget()
        self.list_widget.setGridSize(QSize(100, 80))
        items = ("个人中心", "帮助中心", '切换账号', '退出')
        for item in items:
            temp_item = QListWidgetItem(item)
            temp_item.setSizeHint(QSize(100, 80))
            self.list_widget.addItem(temp_item)
        v_layout.addLayout(h_layout)
        v_layout.addWidget(self.capacity_bar)
        v_layout.addWidget(self.capacity_info)
        self.v_widget = QWidget(self)
        self.v_widget.setLayout(v_layout)
        main_layout.addWidget(self.v_widget)
        main_layout.addWidget(self.list_widget)
        self.setLayout(main_layout)

        self.v_widget.setObjectName('user_info')
        self.list_widget.setObjectName('user_info')
        self.user_name.setObjectName('transparent')
        self.is_vip.setObjectName('transparent')
        self.capacity_info.setObjectName('transparent')
        

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    win = UserInfoUi()
    win.show()
    sys.exit(app.exec_())


