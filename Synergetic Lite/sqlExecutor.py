'''

Synergetic Lite

sqlExecutor.py

By Nick Patrikeos on 12DEC17

'''

import sqlite3

db = sqlite3.connect('synergetic.db')
cursor = db.cursor()
cursor.execute('PRAGMA foreign_keys = ON')

cmd = input('Query: ')

while cmd:
    try:
        cursor.execute(cmd)
    except:
        print('Invalid query.')
    cmd = input('Query: ')

db.commit()
db.close()
