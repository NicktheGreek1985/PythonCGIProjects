#!/usr/bin/python
print('Content-type: text/html\n')

from DB_Functions import *
import sqlite3
import cgi
import cgitb; cgitb.enable()

startHTML('Live Marks','stylesheet')
db = sqlite3.connect('marks.db')
cursor = db.cursor()
form = cgi.FieldStorage()
assessment = form.getvalue('assessment')
raw_mark = form.getvalue('raw_mark')
percentage = form.getvalue('percentage')
weighting = form.getvalue('weighting')
print(assessment, raw_mark, percentage, weighting)
values = [assessment, raw_mark, percentage, weighting]
print(values)

cursor.execute('INSERT INTO DTH (Assessment, Raw_Mark, Percentage, Weighting) VALUES(?, ?, ?, ?)', values)

print('<h1>Live Student Marks - Teacher Access</h1>')
cursor.execute('SELECT * FROM DTH')
data = cursor.fetchall()
print_Records(data, ['Assessment','Raw Mark','Percentage','Weighting'])



endHTML()
cursor.close()
