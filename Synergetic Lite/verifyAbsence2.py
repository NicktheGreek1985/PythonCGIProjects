#!/usr/bin/python
print('Content-type: text/html\n')

'''

Synergetic Lite

PARENT SIDE

verifyAbsence2.py

Saves verification to the DB, and silences all unverified absences
in that time period.

By Nick Patrikeos on 07JAN18

'''

import cgi
import cgitb; cgitb.enable()
import sqlite3
import datetime
from dbFunctions import *


form = cgi.FieldStorage()
startTime = form.getvalue('startTimeHour') + ':' + form.getvalue('startTimeMinute')
endTime = form.getvalue('endTimeHour') + ':' + form.getvalue('endTimeMinute')
studentID = form.getvalue('studentID')
date = form.getvalue('date')


verification = form.getvalue('verification')

times = {"08:55":0,
         "09:45":1,
         "11:00":2,
         "11:55":3,
         "13:25":4,
         "14:20":5}
print(startTime, endTime)
periods = []
for period in times:
    if startTime <= period <= endTime:
        periods.append(times[period])

print(periods)

values = {'verification':verification, 'date':date, 'studentID':studentID}

db = sqlite3.connect('synergetic.db')
cursor = db.cursor()
cursor.execute('PRAGMA foriegn_keys = ON')
if periods:
    cursor.execute('UPDATE AbsenteesUnverified SET Is_Verified = 1 WHERE Date = :date AND Student = :studentID AND Period >=' +
                    str(min(periods)) + ' AND Period <=' + str(max(periods)), values)

cursor.execute('INSERT INTO AbsenteesVerified (Verification, Start_Time, End_Time, Student) VALUES (?, ?, ?, ?)',
                (verification, date + " " + startTime + ":00", date + " " + endTime + ":00", studentID))

print('<script src="script.js"></script>')
print('<body onload="redirectToParentHomepage()"></body>')

db.commit()
db.close()
