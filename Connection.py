import socket
from PyQt5.QtCore import QObject, QThread

class Connection(QThread):

	def __init__(self):
		self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def login(self,ip_address, port, username, password):
		self.ip_address = ip_address
		self.port = port
		self.conn.connect((ip_address, port))
		self.conn.send(b'123')
		return True


class FileTransThread(QThread):
	def run(self):
		pass


if __name__ == '__main__':
	conn = Connection()
	print(conn.login('127.0.0.1', 9000, 'admin', '123456'))