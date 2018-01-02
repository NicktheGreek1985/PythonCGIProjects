#!/usr/bin/python
print('Content-type: text/html\n')

'''

Synergetic Lite

editClass2.py

Edits class in the DB, provided its new ID is not already existing.

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

oldClassID = form.getvalue('oldClassID')
newClassID = form.getvalue('newClassID')
teacherID = form.getvalue('teacherID')
courseID = form.getvalue('courseID')

values = {'oldClassID':oldClassID,
          'teacherID':teacherID,
          'courseID':courseID,
          'newClassID':newClassID,
}

print('<script src="script.js"></script>')

existingWithID = cursor.execute('SELECT * FROM Classes WHERE Class_ID = :newClassID AND Class_ID != :oldClassID', values)
records = cursor.fetchall()

if newClassID is None:
    print('<body onload=\'classesRedirect(1)\'></body>')
elif records:
    # Already in the DB
    print('<body onload=\'classesRedirect(0)\'></body>')
else:
    # cursor.execute('UPDATE Courses SET Course_ID = :newCourseID WHERE Course_ID = :oldCourseID', values)
    cursor.execute('UPDATE Classes SET Class_ID = :newClassID, Teacher = :teacherID, Course = :courseID WHERE Class_ID = :oldClassID', values)
    print('<body onload=\'classesRedirect(2)\'></body>')

db.commit()
db.close()
