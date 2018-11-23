/*************************************************
 # @file   LoginUi
 # @email  642212607@qq.com
 # @date   2018-11-24
*************************************************/

from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QGridLayout, QLineEdit,
							 QCheckBox, QVBoxLayout, QHBoxLayout, QSizePolicy)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import pyqtSignal, Qt, QObject

class LoginUi(QWidget):

	__width__ = 0
	__heigth__ = 0

	def __init__(self, size):
		super(LoginUi, self).__init__()
		self.setWindowFlag(Qt.FramelessWindowHint)
		self.__width__ = size[0]/4
		self.__height__ = size[1]/2
		self.resize(self.__width__, self.__height__)

	def setupUi(self):
		self.setting_button = QPushButton()
		self.minimize_button = QPushButton()
		self.close_button = QPushButton()
		self.logo = QLabel()
		self.user_logo = QLabel()
		self.password_logo = QLabel()
		self.username_line = QLineEdit()
		self.password_line = QLineEdit()
		self.register_button = QPushButton()
		self.find_password_button = QPushButton()
		self.is_rember_checkbox = QCheckBox()
		self.is_autologin_checkbox = QCheckBox()
		self.login_button = QPushButton()

		factor = self.__width__/12
		self.logo.setAlignment(Qt.AlignHCenter)
		self.username_line.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
		self.password_line.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
		self.login_button.setFixedHeight(factor*2.5)
		self.username_line.setFixedWidth(factor*5)
		self.password_line.setFixedWidth(factor*5)

		main_layout = QVBoxLayout()
		main_layout.setContentsMargins(0, 0, 0, factor)
		tools_layout = QHBoxLayout()
		tools_layout.setSpacing(0)
		tools_layout.addWidget(self.setting_button)
		tools_layout.addWidget(self.minimize_button)
		tools_layout.addWidget(self.close_button)
		tools_layout.setAlignment(Qt.AlignRight)
		main_layout.addLayout(tools_layout)
		main_layout.addWidget(self.logo)
		user_layout = QHBoxLayout()
		user_layout.addWidget(self.user_logo)
		user_layout.addWidget(self.username_line)
		user_layout.addWidget(self.register_button)		
		password_layout = QHBoxLayout()
		password_layout.addWidget(self.password_logo)
		password_layout.addWidget(self.password_line)
		password_layout.addWidget(self.find_password_button)
		checkbox_layout = QHBoxLayout()
		checkbox_layout.addWidget(self.is_rember_checkbox)
		checkbox_layout.addWidget(self.is_autologin_checkbox)
		v_layout = QVBoxLayout()
		v_layout.addLayout(user_layout)
		v_layout.addLayout(password_layout)
		v_layout.addStretch(3)
		v_layout.addLayout(checkbox_layout)
		v_layout.setContentsMargins(factor*2, 0, factor*2, factor)
		main_layout.addLayout(v_layout)
		h_layout = QHBoxLayout()
		h_layout.addWidget(self.login_button)
		h_layout.setContentsMargins(factor, 0, factor, factor)
		main_layout.addLayout(h_layout)
		self.setLayout(main_layout)

		self.set_text_and_picture(factor)

	def set_text_and_picture(self, factor):
		self.register_button.setText('注册账户')
		self.find_password_button.setText('找回密码')
		self.is_rember_checkbox.setText('记住密码')
		self.is_autologin_checkbox.setText('自动登录')
		self.login_button.setText('登录')
		self.setting_button.setIcon(QIcon(QPixmap('./source/pic/setting.png')\
			.scaled(factor, factor)))
		self.minimize_button.setIcon(QIcon(QPixmap('./source/pic/hide.png')\
			.scaled(factor, factor)))
		self.close_button.setIcon(QIcon(QPixmap('./source/pic/close.png')\
			.scaled(factor, factor)))
		self.logo.setPixmap(QPixmap('./source/pic/logo.png')\
			.scaled(factor*5, factor*5))
		self.user_logo.setPixmap(QPixmap('./source/pic/user.png')\
			.scaled(factor, factor))
		self.password_logo.setPixmap(QPixmap('./source/pic/password.png')\
			.scaled(factor, factor))


if __name__ == '__main__':
	import sys
	import qdarkstyle
	app = QApplication(sys.argv)
	app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
	width = QApplication.desktop().screenGeometry().width()
	height = QApplication.desktop().screenGeometry().height()
	login = LoginUi([width, height])
	login.setupUi()
	login.show()
	sys.exit(app.exec_())
