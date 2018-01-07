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
studentID = form.getvalue('studentID')

db = sqlite3.connect('synergetic.db')
cursor = db.cursor()
cursor.execute('PRAGMA foriegn_keys = ON')


startHTML('Synergetic Lite', 'main')

print('''<h1>Verify New Absence</h1>
        <hr>
        <div class="mainSection">
            <div class="formContainer">
                <form action="verifyAbsence2.py">
                    Date <input type="text" name="date" placeholder="YY-MM-DD"/><br>
                    Start Time <input type="text" name="startTimeHour" placeholder="HH"/> : <input type="text" name="startTimeMinute" placeholder="MM"/><br>
                    End Time <input type="text" name="endTimeHour"  placeholder="HH" /> : <input type="text" name="endTimeMinute" placeholder="MM"/><br><br>
                    <textarea name="verification" placeholder="Reason/s for absence"></textarea><br><br>
                    <input type="text" style="display:none" name="studentID" value="''' + str(studentID) + '''" />
                    <input type="submit" />
                </form>
            </div>
        </div>''')

print('<hr>')

endHTML()
