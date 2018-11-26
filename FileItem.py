# -*- coding:utf-8 -*-

import os
from resource import source_rc
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, 
                             QGridLayout, QMessageBox, QSizePolicy, QVBoxLayout)
from PyQt5.QtCore import QSettings, Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap

class FileItem(QWidget):

    upload_signal = pyqtSignal(list, str)
    # file_type True为文件 False为文件夹
    def __init__(self, name, is_file):
        super(FileItem, self).__init__()
        self.setAcceptDrops(True)
        self.file_name = name
        self.file_type = os.path.splitext(name)[-1][1:]
        self.is_file = is_file

        self.image_label = QLabel()
        self.name_label = QLabel(name)

        if is_file:
            self.image_label.setPixmap(QPixmap(':/filetype/%s.png' % self.file_type))
        else:
            self.image_label.setPixmap(QPixmap(':/filetype/folder.png'))
        self.image_label.setAlignment(Qt.AlignCenter)
        self.name_label.setAlignment(Qt.AlignCenter)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.image_label)
        main_layout.addWidget(self.name_label)

        self.setLayout(main_layout)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()

    def dropEvent(self, event):
        path_list = [url.path()[1:] for url in event.mimeData().urls()]
        if not self.is_file:
            target_folder = self.file_name
            print(path_list, target_folder)
            self.upload_signal.emit(path_list, target_folder)
        else:
            print('拖拽到了文件上')
        # print('用户拖拽', path_list, '到', target_folder)
        # self.upload_signal.emit(path_list, target_folder)


if __name__ == '__main__':
    import sys
    import qdarkstyle
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    win = FileItem('hello.txt', '0')
    win.show()
    sys.exit(app.exec_())