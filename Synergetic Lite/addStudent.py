#!/usr/bin/python
print('Content-type: text/html\n')

'''

Synergetic Lite

addStudent.py

Adds a new student to the DB, provided its ID is not already existing.

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

studentID = form.getvalue('studentID')
values = {'studentID':studentID}

print('<script src="script.js"></script>')

existingWithID = cursor.execute('SELECT * FROM Students WHERE Student_ID = :studentID', values)
records = cursor.fetchall()

if studentID is None:
    print('<body onload=\'studentsRedirect(1)\'></body>')
    ## Redirect as ID is NONE
    pass
elif records:
    print('<body onload=\'studentsRedirect(0)\'></body>')
    ## Redirect as ID is pre-existing
    pass
else:
    cursor.execute('INSERT INTO Students (Student_ID, Password) VALUES (?, ?)', (studentID, studentID+studentID))
    #cursor.execute('INSERT INTO Courses (Course_ID) VALUES (?)', (courseID,))
    print('<body onload=\'studentsRedirect(2)\'></body>')
    ## Redirect as succeeded


db.commit()
db.close()
