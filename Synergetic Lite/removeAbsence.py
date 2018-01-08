#!/usr/bin/python
print('Content-type: text/html\n')

'''

Synergetic Lite

PARENT SIDE

removeAbsence.py

Allows parent to delete an absence, and any verification for UnverifiedAbsences it caused is removed

By Nick Patrikeos on 08JAN18

'''

import cgi
import cgitb; cgitb.enable()
import sqlite3
import datetime
from dbFunctions import *

form = cgi.FieldStorage()
absenceID = form.getvalue('absenceID')
values = {'absenceID':absenceID}

db = sqlite3.connect('synergetic.db')
cursor = db.cursor()
cursor.execute('PRAGMA foriegn_keys = ON')

cursor.execute('SELECT Start_Time, End_Time, Student FROM AbsenteesVerified WHERE Absentee_V_ID = :absenceID', values)
startTime, endTime, studentID = cursor.fetchall()[0]
print(startTime, endTime)
startDate, startTime = startTime.split(' ')
endDate, endTime = endTime.split(' ')
values['startDate'] = startDate
values['studentID'] = studentID

times = {"08:55":0,
         "09:45":1,
         "11:00":2,
         "11:55":3,
         "13:25":4,
         "14:20":5}

periods = []
for period in times:
    if startTime <= period <= endTime:
        periods.append(times[period])
print(periods)


if periods:
    cursor.execute('UPDATE AbsenteesUnverified SET Is_Verified = 0 WHERE Date = :startDate AND Student = :studentID AND Period >=' +
                    str(min(periods)) + ' AND Period <=' + str(max(periods)), values)

cursor.execute('DELETE FROM AbsenteesVerified WHERE Absentee_V_ID = :absenceID', values)

print('<script src="script.js"></script>')
print('<body onload="redirectToParentHomepage()"></body>')

db.commit()
db.close()
