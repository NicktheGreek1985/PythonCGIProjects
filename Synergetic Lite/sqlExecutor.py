import sqlite3

db = sqlite3.connect('synergetic.db')
cursor = db.cursor()

cmd = input('Query: ')

while cmd:
    try:
        cursor.execute(cmd)
    except:
        print('Invalid query.')
    cmd = input('Query: ')

db.commit()
db.close()
