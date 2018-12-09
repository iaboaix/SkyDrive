# -*- coding:utf-8 -*-

"""
@project: SkyDrive
@file: SkyDrive.py
@author: dangzhiteng
@email: 642212607@qq.com
@date: 2018-11-23
"""

import os
import time
import socket
from queue import Queue
from Tools import get_pixmap
from resource import source_rc
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QProgressBar, \
                            QHBoxLayout, QPushButton, QLabel, QApplication, \
                            QVBoxLayout, QWidget, QRubberBand, QStackedWidget
from PyQt5.QtGui import QIcon, QPixmap, QColor, QDrag, QPainter, QCursor, QDesktopServices
from PyQt5.QtCore import Qt, QSize, QPoint, QRect, pyqtSignal, QThread, QUrl, QSettings, QObject

class TransListWidget(QWidget):

    def __init__(self, *args, **kwargs):
        super(TransListWidget, self).__init__(*args, **kwargs)
        main_layout = QHBoxLayout()
        self.left_menu_widget = LeftMenuWidget()
        self.download_widget = TransWidget('DOWN')
        self.upload_widget = TransWidget('UP')
        self.finished_widget = FinishedWidget()

        self.stack_widget = QStackedWidget(self)
        self.stack_widget.addWidget(self.download_widget)
        self.stack_widget.addWidget(self.upload_widget)
        self.stack_widget.addWidget(self.finished_widget)

        main_layout.addWidget(self.left_menu_widget)
        main_layout.addWidget(self.stack_widget)
        self.setLayout(main_layout)
        main_layout.setStretchFactor(self.left_menu_widget, 1)
        main_layout.setStretchFactor(self.stack_widget, 5)
        self.left_menu_widget.setObjectName('select_type')

        self.left_menu_widget.item_click_signal.connect(self.stack_widget.setCurrentIndex)
        self.upload_widget.item_count_signal.connect(self.update_left_menu)
        self.download_widget.item_count_signal.connect(self.update_left_menu)

    def update_left_menu(self, count):
        sender = QObject.sender(self)
        if sender is self.download_widget:
            if count != 0:
                text = '正在下载({})'.format(count)
            else:
                text = '正在下载'
            self.left_menu_widget.item(0).setText(text)
        elif sender is self.upload_widget:
            if count != 0:
                text = '正在上传({})'.format(count)
            else:
                text = '正在上传'
            self.left_menu_widget.item(1).setText(text)
        else:
            pass


class TransWidget(QStackedWidget):

    port_dict = dict()
    item_count_signal = pyqtSignal(int)
    reday_up_signal = pyqtSignal(str, str)
    reday_down_signal = pyqtSignal(str)
    item_count = 0
    total_size = 0
    trans_size = 0
    def __init__(self, mode):
        super(TransWidget, self).__init__()
        self.factor = QApplication.desktop().screenGeometry().width()/100
        self.mode = mode
        self.empty_widget = QWidget()
        empty_layout = QVBoxLayout()
        self.empty_image = QLabel()
        self.empty_image.setPixmap(QPixmap(':/default/default_pngs/sleep.png'))
        self.empty_tip = QLabel()
        self.empty_image.setAlignment(Qt.AlignHCenter | Qt.AlignBottom)
        self.empty_tip.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        empty_layout.addWidget(self.empty_image)
        empty_layout.addWidget(self.empty_tip)
        self.empty_widget.setLayout(empty_layout)
        self.v_widget = QWidget()
        v_layout = QVBoxLayout()
        progress_layout = QHBoxLayout()
        if mode == 'UP':
            progress_label = QLabel('上传总进度')
            self.empty_tip.setText('当前没有上传任务喔~')
        else:
            progress_label = QLabel('下载总进度')
            self.empty_tip.setText('当前没有下载任务喔~')
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.strat_all_button = QPushButton('全部开始')
        self.cancel_all_button = QPushButton('全部取消')
        progress_layout.addWidget(progress_label)
        progress_layout.addWidget(self.progress_bar)
        progress_layout.addWidget(self.strat_all_button)
        progress_layout.addWidget(self.cancel_all_button)
        self.trans_list = QListWidget()
        self.trans_list.setFocusPolicy(Qt.NoFocus)
        v_layout.addLayout(progress_layout)
        v_layout.addWidget(self.trans_list)
        self.v_widget.setLayout(v_layout)
        self.addWidget(self.empty_widget)
        self.addWidget(self.v_widget)

    def add_items(self, file_list, target_path=''):
        if self.mode == 'UP':
            for file_path in file_list:
                file_name = os.path.split(file_path)[-1]
                if os.path.isfile(file_path):
                    self.total_size += os.path.getsize(file_path)
                    list_item = QListWidgetItem('')
                    list_item.setSizeHint(QSize(self.factor * 3, self.factor * 3))
                    widget_item = TransItem('UP', list_item, self.port_dict, file_path, target_path=os.path.join(target_path, file_name))
                    widget_item.reday_up_signal.connect(self.reday_up_signal)
                    widget_item.delete_signal.connect(self.delete_item)
                    widget_item.finish_signal.connect(self.finish_item)
                    widget_item.update_main_progress.connect(self.update_progress)
                    self.trans_list.addItem(list_item)
                    self.trans_list.setItemWidget(self.trans_list.item(self.item_count), widget_item)
                    self.item_count_change('+')
                else:
                    temp_path_list = [os.path.join(file_path, path) for path in os.listdir(file_path)]
                    self.add_items(temp_path_list, target_path)
        else:
            # file_info = [file_name, file_size]
            for file_path, file_size in file_list:
                self.total_size += file_size
                list_item = QListWidgetItem('')
                list_item.setSizeHint(QSize(self.factor * 3, self.factor * 3))
                widget_item = TransItem('DOWN', list_item, self.port_dict, file_path, file_size=file_size)
                widget_item.reday_down_signal.connect(self.reday_down_signal)
                widget_item.delete_signal.connect(self.delete_item)
                widget_item.finish_signal.connect(self.finish_item)
                widget_item.update_main_progress.connect(self.update_progress)
                self.trans_list.addItem(list_item)
                self.trans_list.setItemWidget(self.trans_list.item(self.item_count), widget_item)
                self.item_count_change('+')

    def delete_item(self, item, item_size):
        del_item = self.trans_list.takeItem(self.trans_list.row(item))
        self.trans_list.removeItemWidget(del_item)
        self.item_count_change('-')
        self.total_size -= item_size
        del del_item

    def finish_item(self, item):
        del_item = self.trans_list.takeItem(self.trans_list.row(item))
        self.trans_list.removeItemWidget(del_item)
        del del_item
        self.item_count_change('-')

    def add_port(self, file_name, port):
        self.port_dict[file_name] = port
        print('当前端口字典：', self.port_dict)

    def update_progress(self, size):
        self.trans_size += size
        self.progress_bar.setValue(self.trans_size * 100 / self.total_size)

    def item_count_change(self, mode):
        if mode == '+':
            self.item_count += 1
        else:
            self.item_count -= 1
        if self.item_count == 0:
            self.setCurrentIndex(0)
        else:
            self.setCurrentIndex(1)
        self.item_count_signal.emit(self.item_count)


class TransItem(QWidget):

    delete_signal = pyqtSignal(QListWidgetItem, int)
    finish_signal = pyqtSignal(QListWidgetItem)
    reday_up_signal = pyqtSignal(str, str)
    reday_down_signal = pyqtSignal(str)
    update_main_progress = pyqtSignal(int)
    is_start = False

    def __init__(self, mode, list_item, port_queue, file_path, target_path='', file_size=0):
        super(TransItem, self).__init__()
        self.factor = QApplication.desktop().screenGeometry().width()/100
        self.mode = mode
        if mode == 'UP':
            self._list_item_ = list_item
            self.port_queue = port_queue
            self.file_path = file_path
            self.target_path = target_path
            self.file_name = os.path.split(file_path)[-1]
            self.file_size = os.path.getsize(file_path)
        else:
            self._list_item_ = list_item
            self.port_queue = port_queue
            self.file_path = file_path            
            self.file_name = os.path.split(file_path)[-1]
            self.file_size = file_size
        self.setContentsMargins(0, 0, 0, 0)
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.item_image = QLabel()
        self.item_image.setFixedSize(QSize(self.factor * 2.5, self.factor * 2.5))
        item_layout = QVBoxLayout()
        self.item_name = QLabel()
        self.item_size = QLabel()
        item_layout.addWidget(self.item_name)
        item_layout.addWidget(self.item_size)
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
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
        self.item_size.setText('0KB/' + str(int(self.file_size/1024)) + 'KB')
        self.item_image.setPixmap(get_pixmap(self.file_name, True).scaled(self.item_image.size()))

        self.item_image.setObjectName('transparent')
        self.item_name.setObjectName('transparent')
        self.item_size.setObjectName('transparent')

        self.start_pause_button.toggled.connect(self.start_pause_task)
        self.cancel_button.clicked.connect(self.cancel_task)
        self.open_folder_button.clicked.connect(self.open_folder)

    def start_pause_task(self, check):
        if check:
            if self.is_start:
                self.trans_thread.pause = False
                return
            print('if', check)
            self.is_start = True
            if self.mode == 'UP':
                self.reday_up_signal.emit(self.target_path, str(self.file_size))
                self.trans_thread = TransThread('UP', self.port_queue, self.file_path, self.file_size)
            else:
                self.reday_down_signal.emit(self.file_path)
                self.trans_thread = TransThread('DOWN', self.port_queue, self.file_name, self.file_size)
            self.trans_thread.progress_signal.connect(self.update_progress)
            self.trans_thread.finished.connect(self.finish)
            self.trans_thread.start()
            self.cancel_button.setEnabled(False)
        else:
            print('else', check)
            self.trans_thread.pause = True

    def cancel_task(self):
        self.delete_signal.emit(self._list_item_, self.file_size)

    def open_folder(self):
        folder = os.path.split(self.file_path)[0]
        QDesktopServices.openUrl(QUrl(folder, QUrl.TolerantMode))

    def update_progress(self, temp_size, send_size):
        self.progress_bar.setValue(send_size * 100 / self.file_size)
        self.item_size.setText(str(int(send_size/1024)) + 'KB/' + str(int(self.file_size/1024)) + 'KB')
        self.update_main_progress.emit(temp_size)

    def finish(self):
        self.finish_signal.emit(self._list_item_)


class FinishedWidget(QWidget):

    def __init__(self):
        super(FinishedWidget, self).__init__()
        h_layout = QHBoxLayout()
        self.count = QLabel('已传输0个文件')
        self.clear_history = QPushButton('清除所有记录')
        h_layout.addWidget(self.count)
        h_layout.addWidget(self.clear_history)
        main_layout = QVBoxLayout()
        finished_list = QListWidget()
        main_layout.addLayout(h_layout)
        main_layout.addWidget(finished_list)
        self.setLayout(main_layout)


class LeftMenuWidget(QListWidget):

    item_click_signal = pyqtSignal(int)
    def __init__(self):
        super(LeftMenuWidget, self).__init__()
        self.factor = QApplication.desktop().screenGeometry().width()/100
        self.setViewMode(QListWidget.ListMode)
        self.setFlow(QListWidget.TopToBottom)
        self.setFocusPolicy(Qt.NoFocus)
        self.make_items()
        self.itemClicked.connect(self.item_clicked)

    def make_items(self):
        url = ':/default/default_icons/'
        items = [QListWidgetItem(QIcon(url + 'download.ico'), '正在下载', self),
                 QListWidgetItem(QIcon(url + 'upload.ico'), '正在上传', self),
                 QListWidgetItem(QIcon(url + 'finished.ico'), '传输完成', self)]
        for item in items:
            item.setSizeHint(QSize(self.factor * 3, self.factor * 3.5))
            self.addItem(item)

    def item_clicked(self, item):
        index = self.row(item)
        self.item_click_signal.emit(index)


class TransThread(QThread):

    progress_signal = pyqtSignal(int, int)
    pause = False

    def __init__(self, mode, port_dict, file_path, file_size):
        super(TransThread, self).__init__()
        self.mode = mode
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
        buffer = 1024 * 4
        if self.mode == 'UP':
            with open(self.file_path, 'rb') as file:
                send_size = 0
                while send_size < self.file_size:
                    if self.pause:
                        while True:
                            time.sleep(1)
                            if not self.pause:
                                break
                    data = file.read(buffer)
                    sock.send(data)
                    temp_size = len(data)
                    send_size += temp_size
                    self.progress_signal.emit(temp_size, send_size)
        else:
            if not os.path.exists('./download'):
                os.path.mkdir('./download')
            with open(os.path.join('./download', self.file_name), 'wb') as file:
                recv_size = 0
                while recv_size < self.file_size:
                    if self.pause:
                        while True:
                            time.sleep(1)
                            if not self.pause:
                                break
                    surplus = self.file_size - recv_size
                    if surplus > buffer:
                        data = sock.recv(buffer)
                    else:
                        data = sock.recv(surplus)
                    file.write(data)
                    temp_size = len(data)
                    recv_size += temp_size
                    self.progress_signal.emit(temp_size, recv_size)
        sock.close()
        print(self.file_path, '传输完毕')
        # del self.port_dict[file_name]


if __name__ == '__main__':
    import sys
    import qdarkstyle
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    win = TransListWidget()
    win.show()
    sys.exit(app.exec_())