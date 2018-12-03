# -*- coding:utf-8 -*-
import os
import time
import socket
from queue import Queue
from Tools import get_pixmap
from resource import source_rc
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QProgressBar, \
                            QHBoxLayout, QPushButton, QLabel, QApplication, \
                            QVBoxLayout, QWidget, QRubberBand
from PyQt5.QtGui import QIcon, QPixmap, QColor, QDrag, QPainter, QCursor, QDesktopServices
from PyQt5.QtCore import Qt, QSize, QPoint, QRect, pyqtSignal, QThread, QUrl, QSettings

class TransListWidget(QWidget):

    def __init__(self, *args, **kwargs):
        super(TransListWidget, self).__init__(*args, **kwargs)
        main_layout = QHBoxLayout()
        self.left_menu_widget = LeftMenuWidget()
        self.upload_widget = TransWidget('UP')
        self.download_widget = TransWidget('DOWN')
        main_layout.addWidget(self.left_menu_widget)
        main_layout.addWidget(self.upload_widget)
        self.setLayout(main_layout)
        main_layout.setStretchFactor(self.left_menu_widget, 2)
        main_layout.setStretchFactor(self.upload_widget, 10)
        self.left_menu_widget.setObjectName('select_type')


class TransWidget(QWidget):

    port_dict = dict()
    reday_up_signal = pyqtSignal(str, str, str)
    item_count = 0
    def __init__(self, mode):
        super(TransWidget, self).__init__()
        self.mode = mode
        main_layout = QVBoxLayout()
        progress_layout = QHBoxLayout()
        if mode == 'UP':
            progress_label = QLabel('上传总进度')
        else:
            progress_label = QLabel('下载总进度')
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

    def add_items(self, path_list='', target_folder=''):
        if self.mode == 'UP':
            for file_path in path_list:
                if os.path.isfile(file_path):
                    list_item = QListWidgetItem('')
                    list_item.setSizeHint(QSize(100,100))
                    widget_item = TransItem('UP', list_item, self.port_dict, file_path, target_folder)
                    widget_item.reday_up_signal.connect(self.reday_up_signal)
                    widget_item.delete_signal.connect(self.delete_item)
                    self.trans_list.addItem(list_item)
                    self.trans_list.setItemWidget(self.trans_list.item(self.item_count), widget_item)
                    self.item_count += 1
                else:
                    temp_path_list = [os.path.join(file_path, path) for path in os.listdir(file_path)]
                    self.add_items(temp_path_list, target_folder)
        else:
            print('下载开发')

    def delete_item(self, item):
        del_item = self.trans_list.takeItem(self.trans_list.row(item))
        self.trans_list.removeItemWidget(del_item)
        del del_item

    def add_port(self, file_name, port):
        self.port_dict[file_name] = port
        print(self.port_dict)


class TransItem(QWidget):

    delete_signal = pyqtSignal(QListWidgetItem)
    reday_up_signal = pyqtSignal(str, str, str)
    reday_down_signal = pyqtSignal()

    def __init__(self, mode, list_item, port_queue, file_path, target_folder=''):
        super(TransItem, self).__init__()
        if mode == 'UP':
            self._list_item_ = list_item
            self.port_queue = port_queue
            self.file_path = file_path
            self.target_folder = target_folder
            self.file_name = os.path.split(file_path)[-1]
            self.file_size = os.path.getsize(file_path)
            self.isfile = os.path.isfile(file_path)
            print(file_path, self.file_size)
        else:
            pass
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
        self.item_size.setText('0KB/' + str(self.file_size/1024) + 'KB')
        self.item_image.setPixmap(\
        get_pixmap(self.file_name, self.isfile).scaled(self.item_image.size()))

        self.item_image.setObjectName('transparent')
        self.item_name.setObjectName('transparent')
        self.item_size.setObjectName('transparent')

        self.start_pause_button.toggled.connect(self.start_pause_task)
        self.cancel_button.clicked.connect(self.cancel_task)
        self.open_folder_button.clicked.connect(self.open_folder)

    def start_pause_task(self, check):
        if check:
            self.reday_up_signal.emit(self.file_name, self.target_folder, str(self.file_size))
            self.trans_thread = TransThread(self.port_queue, self.file_path, self.file_size)
            self.trans_thread.progress_signal.connect(self.update_progress)
            self.trans_thread.finished.connect(self.cancel_task)
            self.trans_thread.start()
        else:
            self.trans_thread.pause = True

    def cancel_task(self):
        self.delete_signal.emit(self._list_item_)

    def open_folder(self):
        folder = os.path.split(self.file_path)[0]
        QDesktopServices.openUrl(QUrl(folder, QUrl.TolerantMode))

    def update_progress(self, send_size):
        self.progress_bar.setValue(send_size * 100 / self.file_size)


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

    progress_signal = pyqtSignal(int)
    pause = False

    def __init__(self, port_dict, file_path, file_size):
        super(TransThread, self).__init__()
        self.port_dict = port_dict
        self.file_path = file_path
        self.file_name = os.path.split(file_path)[-1]
        self.file_size = file_size

    def run(self):
        setting = QSettings('gfkd', 'SkyDrive')
        ip_address = setting.value('SkyDrive/ip_address')
        port = 0
        count = 0
        while True:
            try:
                time.sleep(1)
                port = self.port_dict[self.file_name]
                count += 1
                if int(port) != 0:
                    break
            except:
                print('继续等待')
                if count > 3:
                    print('未申请到端口,传输线程无法启动,已退出。')
                    return
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip_address, port))
        with open(self.file_path, 'rb') as file:
            send_size = 0
            while send_size < self.file_size:
                if self.pause:
                    while True:
                        time.sleep(1)
                        if not self.pause:
                            break
                data = file.read(1024)
                sock.send(data)
                send_size += len(data)
                self.progress_signal.emit(send_size)
            print(self.file_path, '上传完毕')


if __name__ == '__main__':
    import sys
    import qdarkstyle
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    win = TransListWidget()
    win.show()
    sys.exit(app.exec_())