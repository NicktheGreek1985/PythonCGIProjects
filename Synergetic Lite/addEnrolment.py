#!/usr/bin/python
print('Content-type: text/html\n')

'''

Synergetic Lite

addEnrolment.py

Adds a new student to a class, provided it is not already in it.

By Nick Patrikeos on 21DEC17

'''

import cgi
import cgitb; cgitb.enable()
import sqlite3
from dbFunctions import *
from random import randint

db = sqlite3.connect('synergetic.db')
cursor = db.cursor()
cursor.execute('PRAGMA foreign_keys = ON')

form = cgi.FieldStorage()

studentID = form.getvalue('studentID')
classID = form.getvalue('classID')
values = {'studentID':studentID, 'classID':classID}

print('<script src="script.js"></script>')

existingWithID = cursor.execute('SELECT * FROM Enrolments WHERE Student = :studentID AND Class = :classID', values)
records = cursor.fetchall()

if studentID is None:
    print('<body onload=\'enrolmentsRedirect(1 "' + classID + '")\'></body>')
    ## Redirect as ID is NONE
    pass
elif records:
    print('<body onload=\'enrolmentsRedirect(0 "' + classID + '")\'></body>')
    ## Redirect as ID is pre-existing
    pass
else:
    cursor.execute('INSERT INTO Enrolments (Student, Class) VALUES (?, ?)', (studentID, classID))
    #cursor.execute('INSERT INTO Courses (Course_ID) VALUES (?)', (courseID,))
    print('<body onload=\'enrolmentsRedirect(2, "' + classID + '")\'></body>')
    ## Redirect as succeeded


db.commit()
db.close()
