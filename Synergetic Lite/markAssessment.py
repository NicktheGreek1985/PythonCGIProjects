#!/usr/bin/python
print('Content-type: text/html\n')

'''

Synergetic Lite

TEACHER SIDE

markAssessment.py

Teacher can add marks for each student in a class for an assessment

By Nick Patrikeos on 03JAN18

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

print('<h1>Mark Assessment</h1>')
print('<hr>')

cursor.execute('SELECT Student FROM Enrolments WHERE Class = :classID', values)
students = cursor.fetchall()

cursor.execute('SELECT Out_Of FROM Assessments WHERE Assessment_ID = :assessmentID', values)
outOf = cursor.fetchall()[0][0]

fieldnames = ['Student', 'Mark']
print('<form action="markAssessment2.py">')

for i in range(len(students)):
    students[i] += ('<input type="text" name="' + str(students[i][0]) +'" />/' + str(outOf),)

print_Records(students, fields=fieldnames)
print('<input type="text" name="assessmentID" style="display: none" value="' + assessmentID + '" />')
print('<input type="text" name="classID" style="display: none" value="' + classID + '" />')
print('<input type="submit" />')
print('</form>')
print('</div>')

print('<hr>')

endHTML()
