#!/usr/bin/python
print('Content-type: text/html\n')

'''

Synergetic Lite

editCourse.py

Allows the user to edit an existing course in the DB.

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

oldCourseID = form.getvalue('oldCourseID')
newCourseID = form.getvalue('newCourseID')

values = {'oldCourseID':oldCourseID, 'newCourseID':newCourseID}

print('<script src="script.js"></script>')

existingWithID = cursor.execute('SELECT * FROM Courses WHERE Course_ID = :newCourseID AND Course_ID != :oldCourseID', values)
records = cursor.fetchall()

if newCourseID is None:
    print('<body onload=\'coursesRedirect(1)\'></body>')
elif records:
    pass
    # print('Already in the DB')
    # The courseID exists in the DB already.
    print('<body onload=\'coursesRedirect(0)\'></body>')
else:
    cursor.execute('UPDATE Courses SET Course_ID = :newCourseID WHERE Course_ID = :oldCourseID', values)
    print('<body onload=\'coursesRedirect(2)\'></body>')

db.commit()
db.close()
