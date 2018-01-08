#!/usr/bin/python
print('Content-type: text/html\n')

'''

Synergetic Lite

PARENT SIDE

editAbsence.py

Parent can edit details for an existing verified absence.

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

times = {0:"08:55",
         1:"09:50",
         3:"11:00",
         4:"11:55",
         5:"13:25",
         6:"14:20"}

cursor.execute('SELECT Verification, Start_Time, End_Time, Student FROM AbsenteesVerified WHERE Absentee_V_ID = :absenceID', values)
records = cursor.fetchall()
verification, startTime, endTime, studentID = records[0]

startHTML('Synergetic Lite', 'main')

print('''<h1>Edit Absence Verification</h1>
        <hr>
        <div class="mainSection">
            <div class="formContainer">
                <form action="editAbsence2.py">
                    Start Date/Time <input type="text" name="startTime" value="''' + startTime +'''"/><br>
                    End Date/Time <input type="text" name="endTime" value="''' + endTime + '''"/><br><br>
                    <textarea name="verification" placeholder="Reason/s for absence" >''' + verification + '''</textarea><br><br>
                    <input type="text" style="display:none" name="absenceID" value="''' + absenceID + '''" />
                    <input type="text" style="display:none" name="studentID" value="''' + str(studentID) + '''" />
                    <input type="submit" />
                </form>
            </div>
        </div>''')

print('<hr>')

endHTML()
