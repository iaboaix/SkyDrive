import socket
import time
from PyQt5.QtCore import QObject, pyqtSignal

class SendThread(QObject):

    new_msg_signal = pyqtSignal(bytes)

    def __init__(self, ip_address='127.0.0.1', port=50005):
        super(SendThread, self).__init__()
        self.ip_address = ip_address
        self.port = port

    def login(self, username, password):
        time.sleep(5)
        return '123'
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect((self.ip, self.port))
            thread = Thread(target=self.send_message, args=('LOGIN',username,md5(password.encode()).hexdigest()))
            thread.start()
        except socket.error:
            return False

    def sendMessage(self, cmd='LOGIN', username='admin', password='123456'):
        senddata = {'CMD': cmd, 
                    'USERNAME': username,
                    'PASSWORD': password,
                    'SOURCE':source,
                    'TARGET':target}
        for key in list(senddata.keys()):
            if senddata[key] == '':
                del senddata['key']
        self.sock.send(bytes(json.dumps(data), encoding='utf-8'))
        recv_data = self.sock.recv(1024).decode()
        self.new_msg_signal.emit(recv_data)

    # def register(self, username, password, question, answer, activeCode):
    #     senddata = {'type': 1, 'userName': username,
    #                 'passWord': md5(password.encode()).hexdigest(), 'question': question,
    #                 'answer': answer, 'activeCode': activeCode}
    #     return self.sendMessage(senddata)

    # def findquestion(self, username):
    #     senddata = {'type': 2, 'userName': username}
    #     self.sock.send(bytes(json.dumps(senddata), encoding='utf-8'))
    #     data = self.sock.recv(1024).decode()
    #     data = json.loads(data)
    #     return data

    # def findpass(self, username, answer, newPassword):
    #     senddata = {'type': 3, 'userName': username, 'answer': answer, 'newPassword': md5(newPassword.encode()).hexdigest()}
    #     self.sock.send(bytes(json.dumps(senddata), encoding='utf-8'))
    #     recvdata = self.sock.recv(1024).decode()
    #     data = json.loads(recvdata)
    #     return data

    # def back(self):
    #     senddata = {'CMD': 'BACK'}
    #     return self.sendMessage(senddata)

    # def put(self, filelist, sizes):
    #     senddata = {'CMD': 'PUT', 'files': filelist, 'sizes': sizes}
    #     self.sock.send(bytes(json.dumps(senddata), encoding='utf-8'))
    #     data = self.sock.recv(1024).decode()
    #     data = json.loads(data)
    #     return data['port']

    # def get(self, filelist, isshare=0):
    #     if isshare == 0:
    #         cmd = 'GET'
    #     else:
    #         cmd = 'SHAREGET'
    #     senddata = {'CMD': cmd,
    #                 'files': filelist}
    #     self.sock.send(bytes(json.dumps(senddata), encoding='utf-8'))
    #     data = self.sock.recv(1024).decode()
    #     data = json.loads(data)
    #     return data['port']

    # def delete(self, filename, filetype):
    #     senddata = {'CMD': 'DELETE', 'fileName':filename,
    #                 'fileType': filetype}
    #     return self.sendMessage(senddata)

    # def rename(self, sourcename, destname):
    #     senddata = {'CMD': 'RENAME', 'sourceName': sourcename, 'destName': destname}
    #     return self.sendMessage(senddata)

    # def makedir(self, dirname):
    #     senddata = {'CMD': 'MAKEDIR', 'dirName': dirname}
    #     return self.sendMessage(senddata)

    # def listinfo(self, dirname=''):
    #     senddata = {'CMD': 'LIST', 'dirName': dirname}
    #     self.sock.send(bytes(json.dumps(senddata), encoding='utf-8'))
    #     recvdata = self.sock.recv(1024*100).decode()
    #     data = json.loads(recvdata)
    #     return data

    # def looksharefile(self, sharecode):
    #     senddata = {'CMD': 'SHARELIST', 'SHARECODE': sharecode}
    #     self.sock.send(bytes(json.dumps(senddata), encoding='utf-8'))
    #     recvdata = self.sock.recv(1024*100).decode()
    #     data = json.loads(recvdata)
    #     return data

    # def move(self, filepath, filetype, destpath='share'):
    #     senddata = {'CMD': 'MOVE', 'filePath': filepath, 'destPath': destpath, 'fileType': filetype}
    #     return self.sendMessage(senddata)

    # def bye(self):
    #     self.sock.close()

