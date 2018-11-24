 # # # # # # # # # # # # # # #
 # @file   LoginUi           #
 # @email  642212607@qq.com  #
 # @date   2018-11-24        #
 # # # # # # # # # # # # # # #


import sys
import qdarkstyle
from Connection import Connection
from LoginUi import LoginUi
from ConfigureUi import ConfigureUi
from MainwindowUi import MainwindowUi 
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import QObject

class SkyDrive(QWidget):

	__connection__ = Connection()
	def __init__(self):
		self.__LoginUi__ = LoginUi()
		self.__ConfigureUi__ = ConfigureUi()
		self.__MainwindowUi__ = MainwindowUi()
		self.__Connection__ = Connection()

		self.__LoginUi__.setting_button.clicked.connect(self.__ConfigureUi__.show)
		self.__LoginUi__.login_button.clicked.connect(self.login)

	def login(self):
		self.__Connection__.login()


	def show(self):
		self.__LoginUi__.show()



if __name__ == '__main__':
	app = QApplication(sys.argv)
	app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
	skydrive = SkyDrive()
	skydrive.show()
	sys.exit(app.exec_())