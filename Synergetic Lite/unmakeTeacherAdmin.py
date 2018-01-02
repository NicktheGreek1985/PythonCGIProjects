#!/usr/bin/python
print('Content-type: text/html\n')

'''

Synergetic Lite

unmakeTeacherAdmin.py

Makes an administrator a normal teacher.

By Nick Patrikeos on 24DEC17

'''

import cgi
import cgitb; cgitb.enable()
import sqlite3
from dbFunctions import *

db = sqlite3.connect('synergetic.db')
cursor = db.cursor()
cursor.execute('PRAGMA foreign_keys = ON')

form = cgi.FieldStorage()

teacherID = form.getvalue('teacherID')
values = {'teacherID':teacherID}

print('<script src="script.js"></script>')

cursor.execute('UPDATE Teachers SET Is_Admin = 0 WHERE Teacher_ID = :teacherID', values)

print('<body onload=\'teachersRedirect(2)\'></body>')

db.commit()
db.close()
