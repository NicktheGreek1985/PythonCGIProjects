#!/usr/bin/python
print('Content-type: text/html\n')

'''

Synergetic Lite

addClass2.py

Adds a new class to the DB, provided its ID is not already existing.

By Nick Patrikeos on 19DEC17

'''

import cgi
import cgitb; cgitb.enable()
import sqlite3
from dbFunctions import *

db = sqlite3.connect('synergetic.db')
cursor = db.cursor()
cursor.execute('PRAGMA foreign_keys = ON')

form = cgi.FieldStorage()

classID = form.getvalue('classID')
teacherID = form.getvalue('teacherID')
courseID = form.getvalue('courseID')

values = {'classID':classID, 'teacherID':teacherID, 'courseID':courseID}

print('<script src="script.js"></script>')

existingWithID = cursor.execute('SELECT * FROM Classes WHERE Class_ID = :classID', values)
records = cursor.fetchall()

if classID is None:
    print('<body onload=\'classesRedirect(1)\'></body>')
elif records:
    # Already in the DB
    print('<body onload=\'classesRedirect(0)\'></body>')
else:
    cursor.execute('INSERT INTO Classes (Class_ID, Teacher, Course) VALUES (?, ?, ?)', (classID, teacherID, courseID))
    print('<body onload=\'classesRedirect(2)\'></body>')

db.commit()
db.close()
