# -*- coding:utf-8 -*-

"""
@project: SkyDrive
@file: SkyDrive.py
@author: dangzhiteng
@email: 642212607@qq.com
@date: 2018-11-23
"""

import os
import json
import time
import shutil
import socket
import random
import sqlite3
import socketserver
from hashlib import md5
from threading import Thread

ROOTPATH = os.path.join(os.getcwd(),'SkyDrive')
CURIP = '127.0.0.1'
PORT = 50005


class MyTCPHandler(socketserver.BaseRequestHandler):
    username = ''
    password = ''
    CURRENTPATH = ROOTPATH
    SHAREPATH = ''
    sharecode = '******'
    totalsize = 0
    # success_data = bytes(json.dumps({'status': True}), encoding='utf-8')
    # fail_date = bytes(json.dumps({'status': False}), encoding='utf-8')
    hash_key = md5(str(time.time()).encode()).hexdigest()


    def handle(self):
        while True:
            login_data = self.request.recv(1024).decode()
            if len(login_data) == 0:
                print(time.strftime('%Y-%m-%d %H:%M:%S'), self.username,'退出')
                return
            try:
                login_data = json.loads(login_data)
            except:
                print(time.strftime('%Y-%m-%d %H:%M:%S'), '非法数据流入')
                return
            # 登录
            if login_data['CMD'] == 'LOGIN':
                try:
                    self.username = login_data['USERNAME'].replace(' ', '')
                    self.password = login_data['PASSWORD'].replace(' ', '')
                except KeyError:
                    print(time.strftime('%Y-%m-%d %H:%M:%S'), '非法构造数据流入')
                    return
                conn = sqlite3.connect('Users.db')
                cursor = conn.cursor()
                selsql = "select username, password, share, totalsize from users \
                          where username = '{0}'".format(self.username)
                cursor.execute(selsql)
                result = cursor.fetchone()
                if result is None:
                    print(time.strftime('%Y-%m-%d %H:%M:%S'), self.username,'未注册尝试登录')
                    self.request.send(bytes(json.dumps({'CMD': 'LOGIN', 'STATUS': False,\
                                            'HASHKEY': self.hash_key}), encoding='utf-8'))
                    return
                else:
                    if self.password != result[1]:
                        print(time.strftime('%Y-%m-%d %H:%M:%S'), self.username, '密码输入错误.')
                        self.request.send(bytes(json.dumps({'CMD': 'LOGIN', 'STATUS': False,\
                                                'HASHKEY': self.hash_key}), encoding='utf-8'))
                        return
                    else:
                        print(time.strftime('%Y-%m-%d %H:%M:%S'), self.username, '登录成功.')
                        self.CURRENTPATH = os.path.join(self.CURRENTPATH, self.username)
                        self.sharecode = result[2]
                        self.totalsize = result[3]
                        login_success_data = bytes(json.dumps({'CMD': 'LOGIN', 'STATUS': True,\
                                                   'HASHKEY': self.hash_key}), encoding='utf-8')
                        self.request.send(login_success_data)
                        self.list(self.CURRENTPATH)
                        break
        while True:
            recv_data = self.request.recv(1024 * 1024)
            if len(recv_data) == 0:
                break
                print(time.strftime('%Y-%m-%d %H:%M:%S'), self.userName, '退出.')
            try:
                data = recv_data.decode()
                json_data = json.loads(data)
            except:
                print(time.strftime('%Y-%m-%d %H:%M:%S'), '异常数据包产生')
                print(data)
            if json_data['CMD'] == 'REDAYUP':
                file_name = json_data['FILENAME']
                file_size = int(json_data['FILESIZE'])
                port_data = {'CMD': 'REDAYUP',
                             'FILENAME': file_name,
                             'PORT': 0}
                trans_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                while True:
                    try:
                        port = random.randrange(50000, 60000)
                        trans_conn.bind((CURIP, port))
                        trans_conn.listen(1)
                        port_data['PORT'] = port
                        print(time.strftime('%Y-%m-%d %H:%M:%S'), '为用户上传 {} 开放了端口: {}'.format(file_name, port))
                        break
                    except:
                        print(port, '端口被占用，重新选择中...')
                self.request.send(bytes(json.dumps(port_data).encode()))
                print(port_data)
                self.conn, addr = trans_conn.accept()
                dowmload_thread = TransThread('UP', self.conn, self.username, \
                                              os.path.join(self.CURRENTPATH, file_name), file_size)
                dowmload_thread.start()

    def list(self, dirname=''):
        send_data = dict()
        send_data['CMD'] = 'LIST'
        send_data['FILELIST'] = dict()
        send_data['OTHERINFO'] = dict()
        for item in os.listdir(self.CURRENTPATH):
            filePath = os.path.join(self.CURRENTPATH, item)
            send_data['FILELIST'][item] = [os.path.isfile(filePath),
                                           os.path.getctime(filePath),
                                           os.path.getmtime(filePath),
                                           os.path.getsize(filePath)]
        used_size = 0
        for root, dirs, files in os.walk(os.path.join(ROOTPATH, self.username)):
            used_size += sum([os.path.getsize(os.path.join(root, name)) for name in files])
        send_data['OTHERINFO']['SHARECODE'] = self.sharecode
        send_data['OTHERINFO']['TOTALSIZE'] = self.totalsize
        send_data['OTHERINFO']['USEDSIZE'] = used_size

        self.request.sendall(bytes(json.dumps(send_data), encoding='utf-8'))


# 传输线程
class TransThread(Thread):
    # fileMd5 = ''
    recvSize = 0
    sendSize = 0
    # md5Data = md5()

    def __init__(self, mode, conn, user_name, file_path, file_size):
        super(TransThread, self).__init__()
        self.mode = mode
        self.conn = conn
        self.user_name = user_name
        self.file_path = file_path
        self.file_size = file_size
        print(file_size)

    def run(self):
        buffer = 1024 * 4
        if self.mode == 'UP':
            # self.fileMd5 = self.cmdData['md5']
            print(self.user_name, '开始上传', self.file_path)
            trans_size = 0
            with open(self.file_path, 'wb') as file:
                while trans_size < self.file_size:
                    surplus = self.file_size - trans_size
                    if surplus > buffer:
                        data = self.conn.recv(buffer)
                    else:
                        data = self.conn.recv(surplus)
                    file.write(data)
                    trans_size += len(data)
            print(self.user_name, '上传完毕', self.file_path)
            self.conn.close()

                    # self.md5Data.update(data)
        # elif self.cmdData['CMD'] == 'GET':
        #     self.files = self.cmdData['files']
        #     sizes = []
        #     for item in self.files:
        #         sizes.append(os.path.getsize(self.currentPath + '\\' + item))
        #     for item, size in zip(self.files, sizes):
        #         print(self.username, '正在下载', item)
        #         transsize = 0
        #         file = open(self.currentPath + '\\' + item, 'rb')
        #         while not transsize == size:
        #             if size - transsize > 1024:
        #                 data = file.read(1024)
        #             else:
        #                 data = file.read(size - transsize)
        #             self.conn.send(data)
        #             transsize += len(data)
        #             # self.md5Data.update(data)
        #         file.close()

#             # 注册账号
#             elif loginData['type'] == 1:
#                 if loginData['activeCode'] != 'gfkd':
#                     self.request.send(self.failData(4))
#                     print(time.strftime('%Y-%m-%d %H:%M:%S'), loginData['userName'], '注册时激活码输入错误')
#                     continue
#                 else:
#                     self.userName = loginData['userName']
#                     self.passWord = loginData['passWord']
#                     self.question = loginData['question']
#                     self.answer = loginData['answer']
#                     conn = sqlite3.connect('Users.db')
#                     findsql = 'SELECT username from users where username = "{0}"'.format(self.userName)
#                     fcur = conn.cursor()
#                     fcur.execute(findsql)
#                     res = fcur.fetchall()
#                     if len(res) != 0:
#                         self.request.send(self.failData(3))
#                         continue
#                     i = 0
#                     while True:
#                         try:
#                             i += 1
#                             share = ''.join([chr(random.randint(65, 90)) for i in range(0, 6)])
#                             inssql = 'INSERT INTO users (username, password, question, answer, share) VALUES (?, ?, ?, ?, ?)'
#                             value = (self.userName, self.passWord, self.question, self.answer, share)
#                             cur = conn.cursor()
#                             cur.execute(inssql, value)
#                             conn.commit()
#                             cur.close()
#                             conn.close()
#                             print(time.strftime('%Y-%m-%d %H:%M:%S'), self.userName, '注册成功.')
#                             os.mkdir(os.path.join(ROOTPATH, self.userName))
#                             os.mkdir(os.path.join(ROOTPATH, self.userName, '我的共享文件夹'))
#                             self.request.send(self.successData)
#                             break
#                         except:
#                             if i == 3:
#                                 self.request.send(self.failData(0))
#                                 conn.close()
#                                 break
#                             print('注册失败,分享码重复,正在重新生成...')
#             # 查找问题
#             elif loginData['type'] == 2:
#                 userName = loginData['userName']
#                 conn = sqlite3.connect('Users.db')
#                 findsql = 'SELECT username, question, answer from users where username = "{0}"'.format(userName)
#                 fcur = conn.cursor()
#                 fcur.execute(findsql)
#                 res = fcur.fetchone()
#                 fcur.close()
#                 conn.close()
#                 if res is None:
#                     self.request.send(self.failData(1))
#                     continue
#                 else:
#                     self.answer = res[2]
#                     data = {'userName': userName, 'question': res[1]}
#                     self.request.send(bytes(json.dumps(data), encoding='utf-8'))
#                     continue
#             # 重置密码
#             elif loginData['type'] == 3:
#                 userName = loginData['userName']
#                 password = loginData['newPassword']
#                 curanswer = loginData['answer']
#                 conn = sqlite3.connect('Users.db')
#                 cur = conn.cursor()
#                 findsql = 'SELECT answer from users where username = "{0}"'.format(userName)
#                 cur.execute(findsql)
#                 answer = cur.fetchone()
#                 print(answer, curanswer)
#                 if answer[0] != curanswer:
#                     self.request.send(self.failData(1))
#                     continue
#                 try:
#                     sql = "update users set password='{0}' where username='{1}'".format(password, userName)
#                     cur.execute(sql)
#                     conn.commit()
#                     self.request.send(self.successData)
#                     cur.close()
#                     conn.close()
#                     print(time.strftime('%Y-%m-%d %H:%M:%S'), userName, '重置密码.')
#                 except:
#                     self.request.send(self.failData(0))
#         while True:
#             temp = self.request.recv(1024 * 1024)
#             if not temp:
#                 self.request.close()
#                 print(time.strftime('%Y-%m-%d %H:%M:%S'), self.userName, '退出.')
#                 return
#             else:
#                 try:
#                     data = temp.decode()
#                     cmdData = json.loads(data)
#                     currentCMD = cmdData['CMD']
#                     if currentCMD == 'LIST':
#                         try:
#                             self.list(cmdData['dirName'])
#                             if cmdData['dirName'] != '':
#                                 print(time.strftime('%Y-%m-%d %H:%M:%S'), self.userName, '进入', cmdData['dirName'])
#                         except:
#                             print(time.strftime('%Y-%m-%d %H:%M:%S'), self.userName, 'LIST失败.')
#                     elif currentCMD == 'BACK':
#                         if self.CURRENTPATH == os.path.join(ROOTPATH, self.userName):  # 已到达家目录
#                             self.request.send(self.failData(0))
#                             print(time.strftime('%Y-%m-%d %H:%M:%S'), self.userName, 'BACK失败.')
#                         else:
#                             self.CURRENTPATH = os.path.split(self.CURRENTPATH)[0]
#                             self.request.send(self.successData)
#                             # print(time.strftime('%Y-%m-%d %H:%M:%S'), self.userName, 'BACK.')
#                     elif currentCMD == 'PUT':
#                         i = 0
#                         while True:
#                             try:
#                                 i += 1
#                                 port = random.randrange(2000, 5000)
#                                 self.conn0 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#                                 self.conn0.bind((CURIP, port))
#                                 self.conn0.listen(1)
#                                 portData = {'port': port}
#                                 self.request.send(bytes(json.dumps(portData).encode()))
#                                 self.conn, address = self.conn0.accept()
#                                 self.putThread = TransThread(self.userName, self.conn, cmdData, self.CURRENTPATH)
#                                 self.putThread.start()
#                                 self.putThread.join()
#                                 time.sleep(0.05)
#                                 self.conn.close()
#                                 break
#                             except:
#                                 if i == 3:
#                                     break
#                                 print('端口被占用，重新选择中,,,')
#                     elif currentCMD in ('GET', 'SHAREGET'):
#                         print(time.strftime('%Y-%m-%d %H:%M:%S'), self.userName, '下载文件.')
#                         i = 0
#                         while True:
#                             try:
#                                 i += 1
#                                 port = random.randrange(2000, 5000)
#                                 self.conn0 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#                                 self.conn0.bind((CURIP, port))
#                                 self.conn0.listen(1)
#                                 print('下载端口打开,监听', port, '中...')
#                                 portData = {'port': port}
#                                 self.request.send(bytes(json.dumps(portData).encode()))
#                                 self.conn, address = self.conn0.accept()
#                                 if currentCMD == 'GET':
#                                     self.getThread = TransThread(self.userName, self.conn, cmdData, self.CURRENTPATH)
#                                 else:
#                                     self.getThread = TransThread(self.userName, self.conn, cmdData, self.SHAREPATH)
#                                 self.getThread.start()
#                                 self.getThread.join()
#                                 time.sleep(0.05)
#                                 self.conn.close()
#                                 break
#                             except:
#                                 if i == 3:
#                                     break
#                                 # print('端口被占用，重新选择中,,,')
#                     elif currentCMD == 'DELETE':
#                         fileName = cmdData['fileName']
#                         fileType = cmdData['fileType']
#                         if fileType is False:
#                             try:
#                                 os.remove(os.path.join(self.CURRENTPATH, fileName))
#                                 self.request.send(self.successData)
#                                 print(time.strftime('%Y-%m-%d %H:%M:%S'), self.userName, '删除', fileName)
#                             except:
#                                 self.request.send(self.failData)
#                                 print(time.strftime('%Y-%m-%d %H:%M:%S'), self.userName, '删除', fileName, '失败')
#                         else:
#                             try:
#                                 shutil.rmtree(os.path.join(self.CURRENTPATH, fileName))
#                                 self.request.send(self.successData)
#                                 print(time.strftime('%Y-%m-%d %H:%M:%S'), self.userName, '删除', fileName)
#                             except:
#                                 self.request.send(self.failData(0))
#                                 print(time.strftime('%Y-%m-%d %H:%M:%S'), self.userName, '删除', fileName, '失败')
#                     elif currentCMD == 'RENAME':
#                         sourceName = cmdData['sourceName']
#                         destName = cmdData['destName']
#                         try:
#                             os.rename(os.path.join(self.CURRENTPATH, sourceName),
#                                       os.path.join(self.CURRENTPATH, destName))
#                             self.request.send(self.successData)
#                             print(time.strftime('%Y-%m-%d %H:%M:%S'), self.userName, '重命名'+sourceName+'为'+destName)
#                         except:
#                             self.request.send(self.failData)
#                             print(time.strftime('%Y-%m-%d %H:%M:%S'), self.userName, '重命名失败.')
#                     elif currentCMD == 'MAKEDIR':
#                         dirName = cmdData['dirName']
#                         try:
#                             os.mkdir(os.path.join(self.CURRENTPATH, dirName))
#                             self.request.send(self.successData)
#                             print(time.strftime('%Y-%m-%d %H:%M:%S'), self.userName, '创建文件夹', dirName)
#                         except:
#                             self.request.send(self.failData)
#                             print(time.strftime('%Y-%m-%d %H:%M:%S'), self.userName, '创建文件夹失败.')
#                     elif currentCMD == 'SHARELIST':
#                         # {'CMD':'SHARELIST', 'SHARECODE':'AFGKSW'}
#                         sharecode = cmdData['SHARECODE']
#                         db = sqlite3.connect('Users.db')
#                         cur = db.cursor()
#                         sql = 'SELECT username FROM users WHERE share = "{0}"'.format(sharecode)
#                         cur.execute(sql)
#                         result = cur.fetchone()
#                         cur.close()
#                         db.close()
#                         if result is None:
#                             self.request.send(self.failData(0))
#                         else:
#                             self.SHAREPATH = os.path.join(ROOTPATH, result[0], '我的共享文件夹')
#                             self.list(dirname=self.SHAREPATH, isshare=1)
#                             print(time.strftime('%Y-%m-%d %H:%M:%S'), self.userName, '查看共享文件夹' + sharecode)
#                     elif currentCMD == 'MOVE':
#                         filepath = cmdData['filePath']
#                         destpath = cmdData['destPath']
#                         filetype = cmdData['fileType']
#                         if destpath == 'share':
#                             try:
#                                 if filetype is True:
#                                     shutil.copytree(os.path.join(self.CURRENTPATH, filepath), os.path.join(self.CURRENTPATH, '我的共享文件夹', filepath))
#                                 else:
#                                     shutil.copyfile(os.path.join(self.CURRENTPATH, filepath), os.path.join(self.CURRENTPATH, '我的共享文件夹', filepath))
#                                 self.request.send(self.successData)
#                                 print(time.strftime('%Y-%m-%d %H:%M:%S'), self.userName, '共享'+ filepath +'到'+destpath)
#                             except:
#                                 self.request.send(self.failData(0))
#                         else:
#                             try:
#                                 shutil.move(os.path.join(self.CURRENTPATH, filepath), os.path.join(self.CURRENTPATH, destpath))
#                                 self.request.send(self.successData)
#                                 print(time.strftime('%Y-%m-%d %H:%M:%S'), self.userName, '移动'+ filepath +'到'+destpath)
#                             except:
#                                 self.request.send(self.failData(0))
#                     else:
#                         print('未识别此命令.')
#                 except:
#                     print('异常数据包', temp.decode(), '产生。')


# # 传输线程
# class TransThread(Thread):
#     # fileMd5 = ''
#     recvSize = 0
#     sendSize = 0
#     # md5Data = md5()

#     def __init__(self, username, conn, cmdData, currentPath):
#         super(TransThread, self).__init__()
#         self.username = username
#         self.conn = conn
#         self.cmdData = cmdData
#         self.currentPath = currentPath

#     def run(self):
#         if self.cmdData['CMD'] == 'PUT':
#             self.filelist = self.cmdData['files']
#             self.sizes = self.cmdData['sizes']
#             # self.fileMd5 = self.cmdData['md5']
#             for item, size in zip(self.filelist, self.sizes):
#                 name = os.path.split(item)[-1]
#                 print(self.username, '正在上传', name)
#                 transsize = 0
#                 file = open(self.currentPath + '\\' + name, 'wb')
#                 while not transsize == size:
#                     if size - transsize > 1024:
#                         data = self.conn.recv(1024)
#                     else:
#                         data = self.conn.recv(size - transsize)
#                     file.write(data)
#                     transsize += len(data)
#                     # self.md5Data.update(data)
#                 file.close()
#         elif self.cmdData['CMD'] == 'GET':
#             self.files = self.cmdData['files']
#             sizes = []
#             for item in self.files:
#                 sizes.append(os.path.getsize(self.currentPath + '\\' + item))
#             for item, size in zip(self.files, sizes):
#                 print(self.username, '正在下载', item)
#                 transsize = 0
#                 file = open(self.currentPath + '\\' + item, 'rb')
#                 while not transsize == size:
#                     if size - transsize > 1024:
#                         data = file.read(1024)
#                     else:
#                         data = file.read(size - transsize)
#                     self.conn.send(data)
#                     transsize += len(data)
#                     # self.md5Data.update(data)
#                 file.close()
#         else:
#             self.files = self.cmdData['files']
#             sizes = []
#             for item in self.files:
#                 sizes.append(os.path.getsize(self.currentPath + '\\' + item))
#             for item, size in zip(self.files, sizes):
#                 print(self.username, '正在下载', item)
#                 transsize = 0
#                 file = open(self.currentPath + '\\' + item, 'rb')
#                 while not transsize == size:
#                     if size - transsize > 1024:
#                         data = file.read(1024)
#                     else:
#                         data = file.read(size - transsize)
#                     self.conn.send(data)
#                     transsize += len(data)
        
        # print('md5', bytes(self.md5Data.hexdigest().encode()))
        # self.conn.send(bytes(self.md5Data.hexdigest().encode()))
        # self.conn.close()

if __name__ == '__main__':
    host, port = CURIP, PORT
    server = socketserver.ThreadingTCPServer((host, port), MyTCPHandler)
    server.serve_forever()  # 开启服务端
