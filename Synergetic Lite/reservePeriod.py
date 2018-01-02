#!/usr/bin/python
print('Content-type: text/html\n')

'''

Synergetic Lite

reservePeriod.py

Allows the user to reserve a period for a particular class, provided
it does not clash with any classes the students or teacher already has.

By Nick Patrikeos on 22DEC17

'''

import cgi
import cgitb; cgitb.enable()
import sqlite3
from dbFunctions import *
import random

form = cgi.FieldStorage()
periodNum = form.getvalue('periodNum')
classID = form.getvalue('classID')
values = {'classID':classID, 'periodNum':periodNum}

db = sqlite3.connect('synergetic.db')
cursor = db.cursor()
cursor.execute('PRAGMA foreign_keys = ON')


### Test for overlaps etc.
## Will be implemented later

cursor.execute('SELECT Teacher FROM Classes WHERE Class_ID = :classID', values)
teacherID = cursor.fetchall()[0][0]


cursor.execute('SELECT * FROM TeacherPeriods WHERE Class = :classID AND Period_Num = :periodNum', values)
existingInTeachers = cursor.fetchall()
cursor.execute('SELECT Student FROM Enrolments WHERE Class = :classID', values)
students = [i[0] for i in cursor.fetchall()]

existingInStudents = False
for student in students:
    values['studentID'] = student
    cursor.execute('SELECT * FROM StudentPeriods WHERE Class = :classID AND Student = :studentID AND Period_Num = :periodNum', values)

    if cursor.fetchall():
        existingInStudents = True
        break

print('<script src="script.js"></script>')

if existingInTeachers or existingInStudents:
    print('<body onload="timetableRedirect(0, \'' + classID + '\')"></body>')
else:
    ## Fix room allocation

    ## Update for students as well

    cursor.execute('INSERT INTO TeacherPeriods (Period_Num, Class, Room, Teacher) VALUES (?, ?, ?, ?)', (periodNum, classID, 'M1', teacherID))
    for student in students:
        cursor.execute('INSERT INTO StudentPeriods (Period_Num, Class, Room, Student) VALUES (?,?,?,?)', (periodNum, classID, 'M1', student))

    print('<body onload="timetableRedirect(2, \'' + classID + '\')"></body>')
db.commit()
db.close()
