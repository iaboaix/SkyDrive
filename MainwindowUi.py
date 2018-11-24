 # # # # # # # # # # # # # # #
 # @file   LoginUi           #
 # @email  642212607@qq.com  #
 # @date   2018-11-24        #
 # # # # # # # # # # # # # # #

from PyQt5.QtWidgets import QApplication, QWidget

class MainwindowUi(QWidget):

    def __init__(self):
        super(MainwindowUi, self).__init__()
        self.factor = self.__width__ = QApplication.desktop().screenGeometry().width()/100
        self.resize(self.factor*100, self.factor*80)
        pass
