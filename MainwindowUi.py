 # # # # # # # # # # # # # # #
 # @file   LoginUi           #
 # @email  642212607@qq.com  #
 # @date   2018-11-24        #
 # # # # # # # # # # # # # # #

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal

class MainwindowUi(QWidget):

	close_signal = pyqtSignal()
	
	def __init__(self):
		super(MainwindowUi, self).__init__()
		self.setWindowTitle('SkyDrive')
		self.setWindowIcon(QIcon('./source/pic/SkyDrive.ico'))


	def closeEvent(self, event):
		self.close_signal.emit()

if __name__ == '__main__':
	import sys
	import qdarkstyle
	app = QApplication(sys.argv)
	app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
	win = MainwindowUi()
	win.show()
	sys.exit(app.exec_())