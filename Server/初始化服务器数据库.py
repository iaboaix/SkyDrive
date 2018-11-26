# -*- coding:utf-8 -*-
import sqlite3
import os
from hashlib import md5
db = sqlite3.Connection('Users.db')
cursor = db.cursor()
sql = '''create table users(
        username TEXT PRIMARY KEY NOT NULL,
        password TEXT NOT NULL,
        question TEXT NOT NULL,
        answer TEXT NOT NULL,
        share TEXT NOT NULL UNIQUE,
        totalsize INT NOT NULL DEFAULT 20
        )'''
cursor.execute(sql)
ins = 'insert into users values(?, ?, ?, ?, ?, ?)'
value = ('admin', md5('123456'.encode()).hexdigest(), '地址', '湖南长沙', 'ABCDE', 20)
os.mkdir('admin')
cursor.execute(ins,value)
db.commit()
