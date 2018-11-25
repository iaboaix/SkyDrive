 # -*- coding:utf-8 -*-
 # # # # # # # # # # # # # # #
 # @file   LoginUi           #
 # @email  642212607@qq.com  #
 # @date   2018-11-24        #
 # # # # # # # # # # # # # # #

from resource import source_rc
from FileItem import FileItem
from PyQt5.QtWidgets import  (QApplication, QWidget, QLabel, QPushButton, \
                              QTableWidget, QVBoxLayout, QHeaderView)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal

class MainwindowUi(QWidget):

    temp_url = None
    __file_count__ = 0
    __table_shape__ = [7, 0]

    upload_signal = pyqtSignal(list)

    def __init__(self):
        super(MainwindowUi, self).__init__()
        self.setAcceptDrops(True)
        self.factor = QApplication.desktop().screenGeometry().width()/100
        self.resize(self.factor*80, self.factor*50)
        self.setWindowTitle('SkyDrive')
        self.setWindowIcon(QIcon(':icons/SkyDrive.ico'))
        self.file_table = QTableWidget(2, 7)
        # 测试
        for i in range(7):
            item = FileItem('test.txt', 1)
            self.file_table.setCellWidget(0, i, item)
        for i in range(7):
            item = FileItem('test.pdf', 1)
            self.file_table.setCellWidget(1, i, item)
        self.__file_count__ = 14

        self.file_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.file_table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.file_table.horizontalHeader().setHidden(True)
        self.file_table.verticalHeader().setHidden(True)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.file_table)

        self.setLayout(main_layout)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()

    def dropEvent(self, event):
        path_list = [url.path()[1:] for url in event.mimeData().urls()]
        print('用户拖拽', path_list)
        self.upload_signal.emit(path_list)



if __name__ == '__main__':
    import sys
    import qdarkstyle
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    win = MainwindowUi()
    win.show()
    sys.exit(app.exec_())