 # -*- coding:utf-8 -*-
 # # # # # # # # # # # # # # #
 # @file   LoginUi           #
 # @email  642212607@qq.com  #
 # @date   2018-11-24        #
 # # # # # # # # # # # # # # #

from resource import source_rc
from FileItem import FileItem
from PyQt5.QtWidgets import  (QApplication, QWidget, QLabel, QPushButton, \
                              QTableWidget, QVBoxLayout, QHeaderView, QTableWidgetItem)
from PyQt5.QtGui import QIcon, QPixmap, QBrush
from PyQt5.QtCore import pyqtSignal, Qt

class MainwindowUi(QWidget):

    temp_url = None
    table_cloumn = 8
    upload_signal = pyqtSignal(list, str)

    def __init__(self):
        super(MainwindowUi, self).__init__()
        self.factor = QApplication.desktop().screenGeometry().width()/100
        self.setWindowTitle('SkyDrive')
        self.setWindowIcon(QIcon(':icons/SkyDrive.ico'))
        self.resize(self.factor*80, self.factor*50)
        self.file_table = QTableWidget(0, 8)
        self.file_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.file_table.horizontalHeader().setHidden(True)
        self.file_table.verticalHeader().setHidden(True)
        # 测试
        # self.item = FileItem('test', 0)
        # self.file_table.setRowHeight(0, 300)
        # self.file_table.setCellWidget(0, 0, self.item)
        # self.
        # for i in range(7):
        #     item = FileItem('test.txt', 1)
        #     self.file_table.setCellWidget(0, i, item)
        # for i in range(7):
        #     item = FileItem('test.pdf', 1)
        #     self.file_table.setCellWidget(1, i, item)
        # self.__file_count__ = 14

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.file_table)

        self.setLayout(main_layout)

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

if __name__ == '__main__':
    import sys
    import qdarkstyle
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    win = MainwindowUi()
    win.show()
    sys.exit(app.exec_())