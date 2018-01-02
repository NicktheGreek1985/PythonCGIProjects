#!/usr/bin/python
print('Content-type: text/html\n')

'''

Synergetic Lite

addCourse.py

Adds a new course to the DB, provided its ID is not already existing.

By Nick Patrikeos on 15DEC17

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

existingWithID = cursor.execute('SELECT * FROM Courses WHERE Course_ID = :courseID', values)
records = cursor.fetchall()

if courseID is None:
    print('<body onload=\'coursesRedirect(1)\'></body>')
elif records:
    # print('Already in the DB')
    # The courseID exists in the DB already.
    print('<body onload=\'coursesRedirect(0)\'></body>')
else:
    cursor.execute('INSERT INTO Courses (Course_ID) VALUES (?)', (courseID,))
    print('<body onload=\'coursesRedirect(2)\'></body>')

db.commit()
db.close()
