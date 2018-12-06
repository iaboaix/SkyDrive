# -*- coding:utf-8 -*-

"""
@project: SkyDrive
@file: SkyDrive.py
@author: dangzhiteng
@email: 642212607@qq.com
@date: 2018-11-23
"""

import os
import socket
import time
import json
from resource import source_rc
from hashlib import md5
from threading import Thread

class Connection:

    hash_key = ''
    def __init__(self, queue):
        super(Connection, self).__init__()
        self.queue = queue
        self.recv_thread = Thread(target=self.recv_message)

    def login(self, ip_address, port, username, password):
        self.username = username
        self.password = md5(password.encode()).hexdigest()
        self.ip_address = ip_address
        self.port = int(port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            print('正在与', self.ip_address, ':', self.port, '建立连接......')
            self.sock.connect((self.ip_address, self.port))
            send_data = {'CMD': 'LOGIN',
                         'USERNAME': username,
                         'PASSWORD': self.password
                        }
            thread = Thread(target=self.send_message, args=(send_data,))
            thread.start()
            self.recv_thread.start()
            print('与', self.ip_address, ':', self.port, '成功建立连接。')
        except socket.error:
            print('与', self.ip_address, ':', self.port, '连接失败！')

    def cd_folder(self, folder_name):
        send_data = {'CMD': 'CD',
                     'USERNAME': self.username,
                     'HASHKEY': self.hash_key,
                     'TARGET':folder_name,
                    }
        thread = Thread(target=self.send_message, args=(send_data,))
        thread.start()        

    def reday_up(self, file_name, target, file_size):
        send_data = {'CMD': 'REDAYUP',
                     'USERNAME': self.username,
                     'HASHKEY': self.hash_key,
                     'FILENAME':file_name,
                     'TARGET':target,
                     'FILESIZE':file_size
                     }
        thread = Thread(target=self.send_message, args=(send_data,))
        thread.start()

    def send_message(self, send_data):
        self.sock.send(bytes(json.dumps(send_data), encoding='utf-8'))

    def recv_message(self):
        while True:
            recv_data = self.sock.recv(1024*1024).decode()
            if len(recv_data) != 0:
                data = json.loads(recv_data)
                if data['CMD'] == 'LOGIN':
                    self.hash_key = data['HASHKEY']
                    print('用户临时身份验证信息为:', self.hash_key)
                self.queue.put(data)
            else:
                print('服务器端已断开连接！')
                break

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

