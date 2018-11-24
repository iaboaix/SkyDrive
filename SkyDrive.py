 # # # # # # # # # # # # # # #
 # @file   LoginUi           #
 # @email  642212607@qq.com  #
 # @date   2018-11-24        #
 # # # # # # # # # # # # # # #


import sys
import qdarkstyle
from queue import Queue
from threading import Thread
from SendThread import SendThread
from HandleThread import HandleThread
from LoginUi import LoginUi
from ConfigureUi import ConfigureUi
from MainwindowUi import MainwindowUi 
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import QObject

class SkyDrive(QObject):


	msg_queue = Queue()

	def __init__(self):
		super(SkyDrive, self).__init__()
		self.__LoginUi__ = LoginUi()
		self.__ConfigureUi__ = ConfigureUi()
		self.__MainwindowUi__ = MainwindowUi()
		self.__HandleThread__ = HandleThread(self.msg_queue)

		self.__LoginUi__.setting_button.clicked.connect(self.__ConfigureUi__.show)
		self.__LoginUi__.login_button.clicked.connect(self.user_login)


	def user_login(self):
		self.__SendThread__ = SendThread(self.__ConfigureUi__.ip_line.text(), \
										 self.__ConfigureUi__.port_line.text())
		self.__SendThread__.new_msg_signal.connect(lambda: msg_queue.put)
		self.__HandleThread__.start()
		# hash_key = self.__SendThread__.login(self.__LoginUi__.username_line.text(), \
		# 						  		 self.__LoginUi__.password_line.text())
		# print('hash_key:', hash_key)
		# if len(hash_key) != 0:
		# 	self.hash_key = hash_key
		# 	self.__LoginUi__.hide()
		# 	self.__MainwindowUi__.show()


	def show(self):
		self.__LoginUi__.show()



if __name__ == '__main__':
	app = QApplication(sys.argv)
	app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
	skydrive = SkyDrive()
	skydrive.show()
	sys.exit(app.exec_())