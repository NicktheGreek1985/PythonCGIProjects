#!/usr/bin/python
print('Content-type: text/html\n')

'''

Synergetic Lite

addTeacher.py

Adds a new teacher to the DB, provided its ID is not already existing.

By Nick Patrikeos on 17DEC17

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

existingWithID = cursor.execute('SELECT * FROM Teachers WHERE Teacher_ID = :teacherID', values)
records = cursor.fetchall()

if teacherID is None:
    print('<body onload=\'teachersRedirect(1)\'></body>')
    ## Redirect as ID is NONE
    pass
elif records:
    print('<body onload=\'teachersRedirect(0)\'></body>')
    ## Redirect as ID is pre-existing
    pass
else:
    cursor.execute('INSERT INTO Teachers (Teacher_ID, Password, Is_Admin) VALUES (?, ?, ?)', (teacherID, teacherID+teacherID, 0))
    #cursor.execute('INSERT INTO Courses (Course_ID) VALUES (?)', (courseID,))
    print('<body onload=\'teachersRedirect(2)\'></body>')
    ## Redirect as succeeded


db.commit()
db.close()
