#!/usr/bin/python
print('Content-type: text/html\n')

'''

Synergetic Lite

PARENT SIDE

viewVerifiedAbsences.py

Allows parent to view all their verifications for absences.

By Nick Patrikeos on 08JAN18

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

cursor.execute('SELECT Start_Time, End_Time, Verification, Absentee_V_ID FROM AbsenteesVerified WHERE Student = :studentID', values)
fieldnames3 = ['Start Time', 'End Time', 'Verification','Actions']
verifiedAbsences = cursor.fetchall()

for a in range(len(verifiedAbsences)):
    verifiedAbsences[a] = (verifiedAbsences[a][0], verifiedAbsences[a][1], verifiedAbsences[a][2], '<form action="editAbsence.py" id="deleteForm"><input type="text" name="absenceID" value="' +
    str(verifiedAbsences[a][3]) + '" /><input type="submit" value="Edit" /></form> <form action="removeAbsence.py" id="deleteForm"><input type="text" name="absenceID" value="' +
    str(verifiedAbsences[a][3]) + '" /><input type="submit" value="Remove" /></form>',)

startHTML('Synergetic Lite', 'main')

print('<h1>Parent Homepage</h1>')

print('<hr>')

print('<div class="mainSection">')
print('<h3>Absences - Verified</h3>')
print_Records(verifiedAbsences, fields=fieldnames3)

print('<a href="parentHomepage.py?parentID=' + parentID + '"><div class="backButton">Back</div></a>')
print('</div>')
print('<hr>')

endHTML()
