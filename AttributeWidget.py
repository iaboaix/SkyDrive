# -*- coding:utf-8 -*-

"""
@project: SkyDrive
@file: SkyDrive.py
@author: dangzhiteng
@email: 642212607@qq.com
@date: 2018-11-23
"""

import time
from Tools import get_pixmap
from Tools import get_size
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QVBoxLayout , QGridLayout, QWidget, QSizePolicy
from PyQt5.QtCore import Qt


class AttributeWidget(QWidget):
    def __init__(self, file_name, file_info, file_loc):
        super(AttributeWidget, self).__init__()
        # file_name  = file_info[0]
        # file_type  = file_info[1]
        # file_loc   = file_info[2]
        # file_size  = file_info[3]
        # file_ctime = file_info[4]
        # file_mtime = file_info[5]
        self.setWindowTitle('属性')
        pixmap = get_pixmap(file_name, file_info[0])

        file_image = QLabel()
        file_name  = QLabel(file_name)
        file_type  = QLabel(str(file_info[0]))
        file_loc   = QLabel(file_loc)
        file_ctime = QLabel(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(file_info[1])))
        file_mtime = QLabel(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(file_info[2])))
        str_size = get_size(file_info[3])
        file_size  = QLabel(str_size)

        h_layout = QHBoxLayout()
        h_layout.addWidget(file_image)
        h_layout.addWidget(file_name)

        grid_layout = QGridLayout()
        grid_layout.addWidget(QLabel('类型：'), 0, 0)        
        grid_layout.addWidget(file_type, 0, 1)        
        grid_layout.addWidget(QLabel('位置：'), 1, 0)
        grid_layout.addWidget(file_loc, 1, 1)
        grid_layout.addWidget(QLabel('大小：'), 2, 0)
        grid_layout.addWidget(file_size, 2, 1)
        grid_layout.addWidget(QLabel('创建时间：'), 3, 0)
        grid_layout.addWidget(file_ctime, 3, 1)
        grid_layout.addWidget(QLabel('修改时间：'), 4, 0)
        grid_layout.addWidget(file_mtime, 4, 1)

        main_layout = QVBoxLayout()
        main_layout.addLayout(h_layout)
        main_layout.addLayout(grid_layout)

        file_image.setPixmap(pixmap)
        file_name.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        file_name.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.setLayout(main_layout)

