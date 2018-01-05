#!/usr/bin/python
print('Content-type: text/html\n')

'''

Synergetic Lite

TEACHER SIDE

markAttendance.py

Allows teacher to double-check absentees and edit if needed before submitting.

By Nick Patrikeos on 05JAN18

'''

import cgi
import cgitb; cgitb.enable()
import sqlite3
from dbFunctions import *

form = cgi.FieldStorage()
classID = form.getvalue('classID')
periodNum = form.getvalue('periodNum')

values = {'classID':classID}
roll = {}

db = sqlite3.connect('synergetic.db')
cursor = db.cursor()
cursor.execute('PRAGMA foreign_keys = ON')

cursor.execute('SELECT Student FROM Enrolments WHERE Class = :classID', values)
students = [ i[0] for i in cursor.fetchall() ]

absentStudents = []

for student in students:
    presence = form.getvalue(str(student))

    if presence != 'on':
        absentStudents.append(student)
        # cursor.execute('INSERT INTO AbsenteesUnverified (Student, Period, Date) VALUES (?, ?, ?)', (student, periodNum, currentDate))

# print('<script src="script.js"></script>')
# print('<body onload="redirectToTeacherHomepage()"></body>')
startHTML('Synergetic Lite', 'main')

print('<h1>Mark Attendance</h1>')

absentStudents = [(i,) for i in absentStudents]
print('<form action="markAttendance3.py">')
print('<p>You are about to mark the following people as absent:</p>')
print('<input type="text" name="classID" style="display: none" value="' + classID + '" />')
print('<input type="text" name="periodNum" style="display: none" value="' + periodNum + '" />')

fieldnames = ['Student']

for i in range(len(absentStudents)):
    absentStudents[i] = ('<input type="text" name="' + str(absentStudents[i][0]) +'" value="absent" style="display:none;"/>' + str(absentStudents[i][0]),)
absentStudents.append(('<a href="markAttendance.py?classID=' + classID +'&periodNum=' + periodNum +'">Retake Attendance</a>',))
absentStudents.append(('<input type="submit" id="attendanceSubmit"/>',))

print_Records(absentStudents, fields=fieldnames)

print('</form>')

print('<a href="markAttendance.py?classID=' + classID +'&periodNum=' + periodNum +'"><div class="backButton">Retake Attendance</div></a>')

print('<hr>')

endHTML()
