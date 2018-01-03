#!/usr/bin/python
print('Content-type: text/html\n')

'''

Synergetic Lite

addAssessment.py

Adds a new assessment to the DB, provided:
- The OutOf and weighting values are numbers
- The weighting + sum of all current assessment weightings <= 100

By Nick Patrikeos on 02JAN18

'''

import cgi
import cgitb; cgitb.enable()
import sqlite3
from dbFunctions import *

db = sqlite3.connect('synergetic.db')
cursor = db.cursor()
cursor.execute('PRAGMA foreign_keys = ON')

def getCurrentAssessmentWeightingsSum(values):
    cursor.execute('SELECT Weighting FROM Assessments WHERE Course = :courseID', values)
    records = cursor.fetchall()

    return sum([ i[0] for i in records ])


form = cgi.FieldStorage()

courseID = form.getvalue('courseID')
assessmentName = form.getvalue('assessmentName')
succeeded = 2

print('<script src="script.js"></script>')

try:
    outOf = float(form.getvalue('outOf'))
except ValueError:
    succeeded = 0

try:
    weighting = float(form.getvalue('weighting'))
except ValueError:
    succeeded = 1

if succeeded == 2:
    values = {'courseID':courseID, 'outOf': outOf, 'weighting': weighting,
                'assessmentName':assessmentName }

    if getCurrentAssessmentWeightingsSum(values) + weighting <= 100:
        cursor.execute('INSERT INTO Assessments (Name, Out_Of, Weighting, Course, Is_Marked) VALUES (?, ?, ?, ?, ?)',
        (assessmentName, outOf, weighting, courseID, 0))
        print('<body onload="assessmentsRedirect(3, \'' + courseID + '\')"></body>')
    else:
        print('<body onload="assessmentsRedirect(2, \'' + courseID + '\')"></body>')
else:
    print('<body onload="assessmentsRedirect(\'' + str(succeeded) +'\', \'' + courseID + '\')"></body>')


db.commit()
db.close()
