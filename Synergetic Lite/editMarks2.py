#!/usr/bin/python
print('Content-type: text/html\n')

'''

Synergetic Lite

TEACHER SIDE

markAssessment2.py

Update all marks marks for class/assessment in DB. If space is blank, sets mark to 0.

By Nick Patrikeos on 04JAN18

'''

import cgi
import cgitb; cgitb.enable()
import sqlite3
from dbFunctions import *

form = cgi.FieldStorage()
classID = form.getvalue('classID')
assessmentID = form.getvalue('assessmentID')

values = {'classID':classID, 'assessmentID': assessmentID}
marks = {}

db = sqlite3.connect('synergetic.db')
cursor = db.cursor()
cursor.execute('PRAGMA foreign_keys = ON')

cursor.execute('SELECT Student FROM Enrolments WHERE Class = :classID', values)
students = [ i[0] for i in cursor.fetchall() ]

for student in students:
    mark = form.getvalue(str(student))

    if mark is None:
        marks[str(student)] = 0
    else:
        marks[str(student)] = mark

    cursor.execute('UPDATE Marks SET Raw_Mark = :rawMark WHERE Student = :studentID AND Assessment = :assessmentID',
                    {'rawMark':mark, 'studentID':student, 'assessmentID':assessmentID})

print('<script src="script.js"></script>')
print('<body onload="marksRedirect(\'' + classID + '\')"></body>')


db.commit()
db.close()
