#!/usr/bin/python
print('Content-type: text/html\n')

'''

Synergetic Lite

PARENT SIDE

editAbsence2.py

Saves updated details to the DB for an absence Verification

By Nick Patrikeos on 08JAN18

'''

import cgi
import cgitb; cgitb.enable()
import sqlite3
import datetime
from dbFunctions import *


form = cgi.FieldStorage()
startDateTime = form.getvalue('startTime')
endDateTime = form.getvalue('endTime')

abort = False
try:

    startDate, startTime = startDateTime.split(' ')
    endTime = endDateTime.split(' ')[1]
except:
    abort = True

if not abort:
    absenceID = form.getvalue('absenceID')
    studentID = form.getvalue('studentID')

    verification = form.getvalue('verification')

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


    values = {'verification':verification, 'startTime':startTime,
    'endTime':endTime, 'studentID':studentID, 'absenceID':absenceID,'startDate':startDate,'startDateTime':startDateTime, 'endDateTime':endDateTime}

    db = sqlite3.connect('synergetic.db')
    cursor = db.cursor()
    cursor.execute('PRAGMA foriegn_keys = ON')
    if periods:
        cursor.execute('UPDATE AbsenteesUnverified SET Is_Verified = 1 WHERE Date = :startDate AND Student = :studentID AND Period >=' +
                        str(min(periods)) + ' AND Period <=' + str(max(periods)), values)

    cursor.execute('UPDATE AbsenteesVerified SET Verification = :verification, Start_Time = :startDateTime, End_Time = :endDateTime WHERE Absentee_V_ID = :absenceID', values)

    print('<script src="script.js"></script>')
    print('<body onload="redirectToParentHomepage()"></body>')

    db.commit()
    db.close()
else:
    print('<script src="script.js"></script>')
    print('<body onload="alert(\'Date/Time must be entered as YYYY-MM-DD HH:MM:SS\'); redirectToParentHomepage()"></body>')
