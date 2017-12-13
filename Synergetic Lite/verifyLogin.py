#!/usr/bin/python
print('Content-type: text/html\n')

import cgi
import cgitb; cgitb.enable()
import sqlite3

form = cgi.FieldStorage()

username = form.getvalue('username')
password = form.getvalue('password')

db = sqlite3.connect('synergetic.db')
cursor = db.cursor()

values = {'username':username, 'password':password}
isStudent = cursor.execute('SELECT * FROM Students WHERE Student_ID = :username AND Password = :password', values)

print(isStudent)
