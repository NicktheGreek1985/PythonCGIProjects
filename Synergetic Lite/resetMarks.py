#!/usr/bin/python
print('Content-type: text/html\n')

'''

Synergetic Lite

TEACHER SIDE

resetMarks.py

Teacher can reset all marks for assessment.

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

db = sqlite3.connect('synergetic.db')
cursor = db.cursor()
cursor.execute('PRAGMA foreign_keys = ON')

startHTML('Synergetic Lite', 'main')


cursor.execute('SELECT Student FROM Enrolments WHERE Class = :classID', values)
students = [ i[0] for i in cursor.fetchall() ]

for student in students:
    cursor.execute('DELETE FROM Marks WHERE Assessment = :assessmentID AND Student = :studentID',
                    {'assessmentID':assessmentID, 'studentID':student})

print('<script src="script.js"></script>')
print('<body onload="marksRedirect(\'' + classID + '\')"></body>')

db.commit()
db.close()
