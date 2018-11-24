import sqlite3
conn = sqlite3.connect('Users.db')
cur = conn.cursor()
sql = 'select * from users'
cur.execute(sql)
print(cur.fetchall())
a = input()
