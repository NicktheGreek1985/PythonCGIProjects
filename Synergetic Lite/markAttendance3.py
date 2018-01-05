#!/usr/bin/python
print('Content-type: text/html\n')

'''

Synergetic Lite

TEACHER SIDE

markAttendance3.py

Saves all unverified absences to the DB.

By Nick Patrikeos on 05JAN18

'''

import cgi
import cgitb; cgitb.enable()
import sqlite3
import datetime
from dbFunctions import *

form = cgi.FieldStorage()
classID = form.getvalue('classID')
periodNum = form.getvalue('periodNum')

values = {'classID':classID, 'periodNum': periodNum}
currentTime = datetime.datetime.now()
currentDate = currentTime.strftime("%Y-%m-%d")

db = sqlite3.connect('synergetic.db')
cursor = db.cursor()
cursor.execute('PRAGMA foreign_keys = ON')

cursor.execute('SELECT Student FROM Enrolments WHERE Class = :classID', values)
students = [ i[0] for i in cursor.fetchall() ]
print(students)
for student in students:
    if form.getvalue(str(student)) is not None:
        cursor.execute('INSERT INTO AbsenteesUnverified (Student, Period, Date) VALUES (?, ?, ?)', (student, periodNum, currentDate))



print('<script src="script.js"></script>')
print('<body onload="redirectToTeacherHomepage()"></body>')


db.commit()
db.close()
