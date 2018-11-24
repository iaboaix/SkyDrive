import socket
from PyQt5.QtCore import QObject, QThread

class Connection(QThread):

	def __init__(self):
		pass

	def login(self):
		self.chat_thread.login()


class FileTransThread(QThread):
	def run(self):
		pass

