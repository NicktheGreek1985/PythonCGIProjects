#!/usr/bin/python
print('Content-type: text/html\n')

from DB_Functions import *
import sqlite3
import cgi
import cgitb; cgitb.enable()

startHTML('Live Marks','stylesheet')
db = sqlite3.connect('marks.db')
cursor = db.cursor()

print('<h1>Live Student Marks</h1>')
cursor.execute('SELECT * FROM DTH')
data = cursor.fetchall()

print_Records(data, ['Assessment','Raw Mark','Percentage','Weighting'])

endHTML()
cursor.close()
