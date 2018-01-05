#!/usr/bin/python
print('Content-type: text/html\n')

'''

Synergetic Lite

TEACHER SIDE

markAttendance.py

Teacher can mark the attendance for a class.

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

db = sqlite3.connect('synergetic.db')
cursor = db.cursor()
cursor.execute('PRAGMA foreign_keys = ON')

periods = [ [0, 1, 2, 3, 4, 5],
            [6, 7, 8, 9, 10, 11],
            [12, 13, 14, 15, 16, 17],
            [18, 19, 20, 21, 22, 23],
            [24, 25, 26, 27, 28, 29]
            ]

weekday = datetime.datetime.today().weekday()
if weekday >= 5 or int(periodNum) not in periods[weekday]:
    ## YOU ARE NOT MARKING ATTENDANCE FOR CORRECT DAY
    print('<script src="script.js"></script>')
    print('<body onload="alertWrongDay()"></body>')
    
else:
    startHTML('Synergetic Lite', 'main')

    print('<h1>Mark Attendance</h1>')
    print('<hr>')

    cursor.execute('SELECT Student FROM Enrolments WHERE Class = :classID', values)
    students = cursor.fetchall()

    fieldnames = ['Student', 'Attendance']
    print('<form action="markAttendance2.py">')

    for i in range(len(students)):
        students[i] += ('<input type="checkbox" name="' + str(students[i][0]) +'" checked/>',)

    print_Records(students, fields=fieldnames)
    print('<input type="text" name="classID" style="display: none" value="' + classID + '" />')
    print('<input type="text" name="periodNum" style="display: none" value="' + periodNum + '" />')
    print('<input type="submit" />')
    print('</form>')
    print('</div>')

    print('<hr>')

    endHTML()
