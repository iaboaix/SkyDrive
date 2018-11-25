 # -*- coding:utf-8 -*-
 # # # # # # # # # # # # # # #
 # @file   LoginUi           #
 # @email  642212607@qq.com  #
 # @date   2018-11-24        #
 # # # # # # # # # # # # # # #

from resource import source_rc
from PyQt5.QtWidgets import QApplication, QWidget

class MainwindowUi(QWidget):

    def __init__(self):
        super(MainwindowUi, self).__init__()
        self.factor = QApplication.desktop().screenGeometry().width()/100
        

    def show(self):
        self.showMaximized()

if __name__ == '__main__':
    import sys
    import qdarkstyle
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    win = MainwindowUi()
    win.show()
    sys.exit(app.exec_())