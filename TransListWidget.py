# -*- coding:utf-8 -*-
import os
import time
from queue import Queue
from Tools import get_pixmap
from resource import source_rc
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QProgressBar, \
                            QHBoxLayout, QPushButton, QLabel, QApplication, \
                            QVBoxLayout, QWidget, QRubberBand
from PyQt5.QtGui import QIcon, QPixmap, QColor, QDrag, QPainter, QCursor, QDesktopServices
from PyQt5.QtCore import Qt, QSize, QPoint, QRect, pyqtSignal, QThread, QUrl

class TransListWidget(QWidget):

    def __init__(self, *args, **kwargs):
        super(TransListWidget, self).__init__(*args, **kwargs)
        main_layout = QHBoxLayout()
        self.left_menu_widget = LeftMenuWidget()
        self.trans_widget = TransWidget()
        main_layout.addWidget(self.left_menu_widget)
        main_layout.addWidget(self.trans_widget)
        self.setLayout(main_layout)
        main_layout.setStretchFactor(self.left_menu_widget, 2)
        main_layout.setStretchFactor(self.trans_widget, 10)
        self.left_menu_widget.setObjectName('select_type')


class TransWidget(QWidget):

    port_queue = Queue()
    request_port = pyqtSignal()
    def __init__(self, *args, **kwargs):
        super(TransWidget, self).__init__(*args, **kwargs)
        main_layout = QVBoxLayout()
        progress_layout = QHBoxLayout()
        progress_label = QLabel('上传总进度')
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(30)
        self.strat_all_button = QPushButton('全部开始')
        self.cancel_all_button = QPushButton('全部取消')
        progress_layout.addWidget(progress_label)
        progress_layout.addWidget(self.progress_bar)
        progress_layout.addWidget(self.strat_all_button)
        progress_layout.addWidget(self.cancel_all_button)
        self.trans_list = QListWidget()
        self.trans_list.setFocusPolicy(Qt.NoFocus)
        main_layout.addLayout(progress_layout)
        main_layout.addWidget(self.trans_list)
        self.setLayout(main_layout)

    def addItems(self, path_list, target_folder):
        for index, file in enumerate(path_list):
            list_item = QListWidgetItem('')
            list_item.setSizeHint(QSize(100,100))
            widget_item = TransItem(list_item, self.port_queue, file, target_folder)
            widget_item.cancel_signal.connect(self.delete_item)
            self.trans_list.addItem(list_item)
            self.trans_list.setItemWidget(self.trans_list.item(index), widget_item)
            widget_item.trans_thread.request_port.connect(self.request_port)

    def delete_item(self, item):
        del_item = self.trans_list.takeItem(self.trans_list.row(item))
        self.trans_list.removeItemWidget(del_item)

    def put_port_queue(self, port):
        self.port_queue.put(port)

class TransItem(QWidget):

    cancel_signal = pyqtSignal(QListWidgetItem)
    def __init__(self, list_item, port_queue, file_path, target_folder):
        super(TransItem, self).__init__()
        self.list_item = list_item
        self.file_path = file_path
        self.target_folder = target_folder
        self.file_name = os.path.split(file_path)[-1]
        self.file_size = os.path.getsize(file_path)/1024
        self.isfile = os.path.isfile(file_path)
        self.trans_thread = TransThread(port_queue)

        self.setContentsMargins(0, 0, 0, 0)
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.item_image = QLabel()
        self.item_image.setFixedSize(QSize(80, 80))
        item_layout = QVBoxLayout()
        self.item_name = QLabel()
        self.item_size = QLabel()
        item_layout.addWidget(self.item_name)
        item_layout.addWidget(self.item_size)
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedWidth(self.width()*0.8)
        # import random
        # self.progress_bar.setValue(random.randint(20 ,50))
        button_layout = QHBoxLayout()
        self.start_pause_button = QPushButton()
        self.cancel_button = QPushButton()
        self.open_folder_button = QPushButton()
        self.start_pause_button.setCheckable(True)
        self.cancel_button.setCheckable(True)
        self.open_folder_button.setCheckable(True)
        self.start_pause_button.setObjectName('start_pause')
        self.cancel_button.setObjectName('cancel')
        self.open_folder_button.setObjectName('folder')
        button_layout.addWidget(self.start_pause_button)
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.open_folder_button)
        main_layout.addWidget(self.item_image)
        main_layout.addLayout(item_layout)
        main_layout.addStretch()
        main_layout.addWidget(self.progress_bar)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

        self.item_name.setText(self.file_name)
        self.item_size.setText('0KB/' + str(self.file_size) + 'KB')
        self.item_image.setPixmap(\
        get_pixmap(self.file_name, self.isfile).scaled(self.item_image.size()))

        self.item_image.setObjectName('transparent')
        self.item_name.setObjectName('transparent')
        self.item_size.setObjectName('transparent')

        self.start_pause_button.toggled.connect(self.start_pause_task)
        self.trans_thread.progress_signal.connect(self.progress_bar.setValue)


        self.cancel_button.clicked.connect(self.cancel_task)
        self.open_folder_button.clicked.connect(self.open_folder)

    def start_pause_task(self, check):
        if check:
            print('获取端口 开始传输')
            self.trans_thread.start()
        else:
            print('暂停任务')

    def cancel_task(self):
        self.cancel_signal.emit(self.list_item)

    def open_folder(self):
        folder = os.path.split(self.file_path)[0]
        QDesktopServices.openUrl(QUrl(folder, QUrl.TolerantMode))


class LeftMenuWidget(QListWidget):

    def __init__(self):
        super(LeftMenuWidget, self).__init__()
        self.setViewMode(QListWidget.ListMode)
        self.setFlow(QListWidget.TopToBottom)
        self.setFocusPolicy(Qt.NoFocus)
        self.make_items()

    def make_items(self):
        url = ':/default/default_icons/'
        items = [QListWidgetItem(QIcon(url + 'recent_normal.ico'), '正在下载', self),
                 QListWidgetItem(QIcon(url + 'files_normal.ico'), '正在上传', self),
                 QListWidgetItem(QIcon(url + 'hide_space_normal.ico'), '传输完成', self)]
        for item in items:
            item.setSizeHint(QSize(100, 80))
            self.addItem(item)

class TransThread(QThread):

    request_port = pyqtSignal()
    progress_signal = pyqtSignal(int)
    def __init__(self, port_queue):
        super(TransThread, self).__init__()
        self.port_queue = port_queue
        pass

    def run(self):
        self.request_port.emit()
        print(self.port_queue.get())



if __name__ == '__main__':
    import sys
    import qdarkstyle
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    win = TransListWidget()
    win.show()
    sys.exit(app.exec_())