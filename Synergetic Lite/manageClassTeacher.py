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

cursor.execute('SELECT Student FROM Enrolments WHERE Class = :classID', values)
students = cursor.fetchall()


print('<hr>')
print('<h2>Student Performance</h2>')

cursor.execute('SELECT Name, Assessment_ID, Out_Of, Weighting FROM Assessments WHERE Course = :courseID', {'courseID':records[0][2]})
assessments = cursor.fetchall()
assessmentNames = ['Student'] + [i[0] for i in assessments ] + ['Average', 'Course Rank']


records = list(students)
assessmentsMarked = []
studentAverages = {}
assessmentAverages = { i[0]:0 for i in assessments }
numStudents = len(students)

for i in range(numStudents):
    studentTotal = 0
    weightingTotal = 0

    for j in assessments:

        cursor.execute('SELECT Raw_Mark FROM Marks WHERE Assessment = :assessmentID AND Student = :studentID',
                        {'assessmentID':str(j[1]), 'studentID':str(students[i][0])})

        try:
            mark = cursor.fetchall()[0][0]

        except:
            records[i] += ('Not Marked',)
            assessmentsMarked.append(False)
            continue

        assessmentsMarked.append(True)
        outOf = j[2]
        studentTotal += (float(mark)/float(outOf) * float(j[3]))
        weightingTotal += float(j[3])

        percentage = int(round(float(mark)/float(outOf) * 100, 0))
        assessmentAverages[j[0]] += percentage

        records[i] += (str(percentage) + "%",)

    studentAverage = int(round((float(studentTotal) / float(weightingTotal)) * 100, 0))
    studentAverages[students[i][0]] = (studentAverage, i)

    records[i] += (str(studentAverage) + "%",)

studentAverages = sorted([ (studentAverages[i][0], studentAverages[i][1]) for i in studentAverages ], reverse=True)

for a in assessmentAverages:
    assessmentAverages[a] = int(round((float(assessmentAverages[a]) / float(numStudents)), 0))

for rank in range(len(studentAverages)):
    loc = studentAverages[rank][1]

    records[loc] += (str(rank + 1),)

avgRow = ('Average',)

finalRow = ('Actions',)

x = 0
for i in assessments:
    #cursor.execute('SELECT AVG(Marks.Raw_Mark) FROM Marks WHERE ')
    #topMark =

    if assessmentsMarked[x]:
        finalRow += ('''<form id="deleteForm" action="editMarks.py">
                    <input type="text" name="classID" value="''' + classID + '''" />
                    <input type="text" name="assessmentID" value="''' + str(i[1]) + '''" />
                    <input type="submit" value="Edit" /></form> <form id="deleteForm" action="resetMarks.py">
                                <input type="text" name="classID" value="''' + classID + '''" />
                                <input type="text" name="assessmentID" value="''' + str(i[1]) + '''" />
                                <input type="submit" value="Reset" /></form>''',)
    else:
        finalRow += ('''<form id="deleteForm" action="markAssessment.py">
                    <input type="text" name="classID" value="''' + classID + '''" />
                    <input type="text" name="assessmentID" value="''' + str(i[1]) + '''" />
                    <input type="submit" value="Mark" /></form>''',)
    x += 1

finalRow += ('','')
records.append(finalRow)

print_Records(records, fields=assessmentNames)

print('<hr>')
print('<div class="backButton" onclick="redirectToTeacherHomepage()">Back</div>')
print('</div>')

print('<hr>')

endHTML()
