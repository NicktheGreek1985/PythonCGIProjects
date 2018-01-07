#!/usr/bin/python
print('Content-type: text/html\n')

'''

Synergetic Lite

PARENT SIDE

viewUnverifiedAbsences.py

Creates HTML page to display:
- All unverified absences, with action to verify

By Nick Patrikeos on 07JAN18

'''

import cgi
import cgitb; cgitb.enable()
import sqlite3
import datetime
from dbFunctions import *


db = sqlite3.connect('synergetic.db')
cursor = db.cursor()
cursor.execute('PRAGMA foreign_keys = ON')

form = cgi.FieldStorage()
parentID = form.getvalue('parentID')
values = {'parentID':parentID}

cursor.execute('SELECT Student FROM Parents WHERE Parent_ID = :parentID', values)
studentID = cursor.fetchall()[0][0]
values['studentID'] = studentID

cursor.execute('SELECT Period, Date, Absentee_U_ID FROM AbsenteesUnverified WHERE Student = :studentID AND NOT Is_Verified', values)
fieldnames1 = ['Period', 'Date','Actions']
absences = cursor.fetchall()

for a in range(len(absences)):
    absences[a] = (int(absences[a][0]) + 1, absences[a][1], '<form id="deleteForm" action="verifyAbsence.py"><input type="text" name="absenceID" value="' + str(absences[a][2]) +'"/>' +
                    '<input type="submit" value="Verify" /></form>',)

startHTML('Synergetic Lite', 'main')

print('<h1>Absences - Unverified</h1>')

print('<hr>')

print_Records(absences, fields=fieldnames1)

print('<a href="parentHomepage.py?parentID=' + parentID + '"><div class="backButton">Back</div></a>')
print('</div>')
print('<hr>')

endHTML()
