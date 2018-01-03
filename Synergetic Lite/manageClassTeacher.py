#!/usr/bin/python
print('Content-type: text/html\n')

'''

Synergetic Lite

TEACHER SIDE

manageClassTeacher.py

Allows teacher to view class details and students, and track student progress

By Nick Patrikeos on 03JAN18

'''

import cgi
import cgitb; cgitb.enable()
import sqlite3
from dbFunctions import *

form = cgi.FieldStorage()
classID = form.getvalue('classID')
values = {'classID':classID}

db = sqlite3.connect('synergetic.db')
cursor = db.cursor()
cursor.execute('PRAGMA foreign_keys = ON')

cursor.execute('SELECT * FROM Classes WHERE Class_ID = :classID',values)
records = cursor.fetchall()
classID = records[0][0]

startHTML('Synergetic Lite', 'main')

print('<h1>Class Management</h1>')

print('<hr>')
print('<div class="mainSection">')
print('<h2>Information</h2>')
print('<p>Class ID</p>')
print('<h3>' + classID + '</h3>')
print('<p>Teacher</p>')
print('<h3>' + records[0][1] + '</h3>')
print('<p>Course</p>')
print('<h3>' + records[0][2] + '</h3>')
print('<hr>')
print('<h2>Students</h2>')

fieldnames = ['ID']
cursor.execute('SELECT Student FROM Enrolments WHERE Class = :classID', values)
students = cursor.fetchall()

print_Records(students, fields=fieldnames)

print('<hr>')
print('<h2>Student Performance</h2>')

cursor.execute('SELECT Name, Assessment_ID, Out_Of FROM Assessments WHERE Course = :courseID', {'courseID':records[0][2]})
assessments = cursor.fetchall()
assessmentNames = ['Student'] + [i[0] for i in assessments ]


records = list(students)
assessmentsMarked = []

for i in range(len(students)):
    for j in assessments:

        cursor.execute('SELECT Raw_Mark FROM Marks WHERE Assessment = :assessmentID AND Student = :studentID',
                        {'assessmentID':str(j[1]), 'studentID':str(students[i][0])})

        try:
            mark = cursor.fetchall()[0][0]
            print(mark)
        except:
            records[i] += ('Not Marked',)
            assessmentsMarked.append(False)
            continue

        assessmentsMarked.append(True)
        outOf = j[2]
        print(outOf)
        percentage = int(round(float(mark)/float(outOf) * 100, 0))

        records[i] += (str(percentage) + "%",)


finalRow = ('Actions',)

x = 0
for i in assessments:
    if assessmentsMarked[x]:
        finalRow += ('<a href="#">Edit</a>',)
    else:
        finalRow += ('''<form id="deleteForm" action="markAssessment.py">
                    <input type="text" name="classID" value="''' + classID + '''" />
                    <input type="text" name="assessmentID" value="''' + str(i[1]) + '''" />
                    <input type="submit" value="Mark" /></form>''',)
    x += 1
records.append(finalRow)

print_Records(records, fields=assessmentNames)

# print('<div class="backButton">Mark Assessment</div>')
print('<hr>')
print('<div class="backButton" onclick="redirectToTeacherHomepage()">Back</div>')
print('</div>')

print('<hr>')

endHTML()
