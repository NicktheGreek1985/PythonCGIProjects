#!/usr/bin/python
print('Content-type: text/html\n')

'''

Synergetic Lite

removePeriodReservation.py

Allows the user to "un-reserve" a period for all students and teachers in a class.

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

cursor.execute('SELECT Teacher FROM Classes WHERE Class_ID = :classID', values)
teacherID = cursor.fetchall()[0][0]

print('<script src="script.js"></script>')

cursor.execute('DELETE FROM TeacherPeriods WHERE Class = :classID AND Period_Num = :periodNum', values)

cursor.execute('SELECT Student FROM Enrolments WHERE Class = :classID', values)
students = [i[0] for i in cursor.fetchall()]

for student in students:
    values['studentID'] = student
    cursor.execute('DELETE FROM StudentPeriods WHERE Class = :classID AND Student = :studentID AND Period_Num = :periodNum', values)


print('<body onload="timetableRedirect(2, \'' + classID + '\')"></body>')
db.commit()
db.close()
