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

class MainwindowUi(QWidget):

    __file_count__ = 0
    __table_shape__ = [7, 0]
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

        self.file_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.file_table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.file_table.horizontalHeader().setHidden(True)
        self.file_table.verticalHeader().setHidden(True)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.file_table)

        self.setLayout(main_layout)

    def mouseReleaseEvent(self, event):
            print(event.mimeData().urls())



if __name__ == '__main__':
    import sys
    import qdarkstyle
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    win = MainwindowUi()
    win.show()
    sys.exit(app.exec_())