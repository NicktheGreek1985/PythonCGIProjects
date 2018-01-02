#!/usr/bin/python
print('Content-type: text/html\n')

'''

Synergetic Lite

deleteStudent.py

Deletes a student from the DB.

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

studentID = form.getvalue('studentID')
values = {'studentID':studentID}

print('<script src="script.js"></script>')

cursor.execute('DELETE FROM Students WHERE Student_ID = :studentID', values)

print('<body onload=\'studentsRedirect(2)\'></body>')

db.commit()
db.close()
