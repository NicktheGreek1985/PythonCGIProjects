#!/usr/bin/python
print('Content-type: text/html\n')

'''

Synergetic Lite

deleteAssessment.py

Deletes an assessment from the DB

By Nick Patrikeos on 03JAN18

'''

import cgi
import cgitb; cgitb.enable()
import sqlite3
from dbFunctions import *

db = sqlite3.connect('synergetic.db')
cursor = db.cursor()
cursor.execute('PRAGMA foreign_keys = ON')

form = cgi.FieldStorage()

assessmentID = form.getvalue('assessmentID')
values = {'assessmentID':assessmentID}

print('<script src="script.js"></script>')

cursor.execute('SELECT Course FROM Assessments WHERE Assessment_ID = :assessmentID', values)
courseID = cursor.fetchall()[0][0]

cursor.execute('DELETE FROM Assessments WHERE Assessment_ID = :assessmentID', values)

print('<body onload=\'assessmentsRedirect(3, "' + courseID + '")\'></body>')

db.commit()
db.close()
