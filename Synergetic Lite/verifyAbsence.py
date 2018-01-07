#!/usr/bin/python
print('Content-type: text/html\n')

'''

Synergetic Lite

PARENT SIDE

verifyAbsence.py

Parent can verify an unverified absence for a student

By Nick Patrikeos on 07JAN18

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

times = {0:"08:55",
         1:"09:50",
         3:"11:00",
         4:"11:55",
         5:"13:25",
         6:"14:20"}

cursor.execute('SELECT Period, Date, Student FROM AbsenteesUnverified WHERE Absentee_U_ID = :absenceID', values)
records = cursor.fetchall()
startTime = times[int(records[0][0])]
endTime = times[int(records[0][0]) + 1]
startTimeHour, startTimeMinute = startTime.split(':')
endTimeHour, endTimeMinute = endTime.split(':')

startHTML('Synergetic Lite', 'main')

print('''<h1>Verify Existing Absence</h1>
        <hr>
        <div class="mainSection">
            <div class="formContainer">
                <form action="verifyAbsence2.py">
                    Date <input type="text" name="date" value="''' + records[0][1] + '''"/><br>
                    Start Time <input type="text" name="startTimeHour" value="''' + startTimeHour +'''"/> : <input type="text" name="startTimeMinute" value="''' + startTimeMinute + '''"/><br>
                    End Time <input type="text" name="endTimeHour" value="''' + endTimeHour + '''"/> : <input type="text" name="endTimeMinute" value="''' + endTimeMinute + '''"/><br><br>
                    <textarea name="verification" placeholder="Reason/s for absence"></textarea><br><br>
                    <input type="text" style="display:none" name="studentID" value="''' + str(records[0][2]) + '''" />
                    <input type="submit" />
                </form>
            </div>
        </div>''')

print('<hr>')

endHTML()
