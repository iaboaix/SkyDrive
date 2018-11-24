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
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
from PyQt5.QtCore import QObject
from PyQt5.QtGui import QIcon

class SkyDrive(QWidget):

	__connection__ = Connection()
	def __init__(self):
		super(SkyDrive, self).__init__()
		self.setWindowTitle('SkyDrive')
		self.setWindowIcon(QIcon('./source/pic/SkyDrive.ico'))
		self.__LoginUi__ = LoginUi()
		self.__ConfigureUi__ = ConfigureUi()
		self.__MainwindowUi__ = MainwindowUi()
		self.__Connection__ = Connection()

		self.__LoginUi__.setting_button.clicked.connect(self.__ConfigureUi__.show)
		self.__LoginUi__.login_button.clicked.connect(self.login)
		self.__MainwindowUi__.close_signal.connect(self.__LoginUi__show)

	def login(self):
		if self.__Connection__.login(self.__LoginUi__.username_line.text(),
									 self.__LoginUi__.password_line.text()):
			self.__LoginUi__.hide()
			self.__MainwindowUi__.show()
		else:
			QMessageBox.warning(self, 'Warning', '用户名或密码错误！')



	def show(self):
		self.__LoginUi__.show()



if __name__ == '__main__':
	app = QApplication(sys.argv)
	app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
	skydrive = SkyDrive()
	skydrive.show()
	sys.exit(app.exec_())