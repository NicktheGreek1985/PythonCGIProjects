#!/usr/bin/python
print('Content-type: text/html\n')

'''

Synergetic Lite

deleteEnrolment.py

Deletes an enrolment from the DB.

By Nick Patrikeos on 21DEC17

'''

import cgi
import cgitb; cgitb.enable()
import sqlite3
from dbFunctions import *

db = sqlite3.connect('synergetic.db')
cursor = db.cursor()
cursor.execute('PRAGMA foreign_keys = ON')

form = cgi.FieldStorage()

classID = form.getvalue('classID')
studentID = form.getvalue('studentID')
values = {'classID':classID, 'studentID':studentID}

print('<script src="script.js"></script>')

cursor.execute('DELETE FROM Enrolments WHERE Class = :classID AND Student = :studentID', values)

print('<body onload=\'enrolmentsRedirect(2, "' + classID + '")\'></body>')

db.commit()
db.close()
