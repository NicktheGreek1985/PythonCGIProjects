#!/usr/bin/python
print('Content-type: text/html\n')

'''

Synergetic Lite

deleteCourse.py

Deletes a course from the DB

By Nick Patrikeos on 16DEC17

'''

import cgi
import cgitb; cgitb.enable()
import sqlite3
from dbFunctions import *

db = sqlite3.connect('synergetic.db')
cursor = db.cursor()
cursor.execute('PRAGMA foreign_keys = ON')

form = cgi.FieldStorage()

courseID = form.getvalue('courseID')
values = {'courseID':courseID}

print('<script src="script.js"></script>')

cursor.execute('DELETE FROM Courses WHERE Course_ID = :courseID', values)

print('<body onload=\'coursesRedirect(2)\'></body>')

db.commit()
db.close()
