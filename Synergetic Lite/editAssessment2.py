#!/usr/bin/python
print('Content-type: text/html\n')

'''

Synergetic Lite

editAssessment2.py

Edits an existing assessment to the DB, provided:
- The OutOf and weighting values are numbers
- The weighting + sum of all current assessment weightings <= 100

Adds a new class to the DB, provided its ID is not already existing.

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

assessmentID = form.getvalue('assessmentID')
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
    values = {'assessmentID':assessmentID, 'outOf': outOf, 'weighting': weighting,
                'name':assessmentName }


    cursor.execute('SELECT Course FROM Assessments WHERE Assessment_ID = :assessmentID', values)
    courseID = cursor.fetchall()[0][0]

    values['courseID'] = courseID

    if getCurrentAssessmentWeightingsSum(values) + weighting <= 100:
        cursor.execute('INSERT INTO Assessments (Name, Out_Of, Weighting, Course) VALUES (?, ?, ?, ?)',
        (assessmentName, outOf, weighting, courseID))

        cursor.execute('UPDATE Assessments SET Name = :name, Out_Of = :outOf, weighting = :weighting WHERE Assessment_ID = :assessmentID', values)

        print('<body onload="assessmentsRedirect(3, \'' + courseID + '\')"></body>')

    else:
        print('<body onload="assessmentsRedirect(2, \'' + courseID + '\')"></body>')
else:
    print('<body onload="assessmentsRedirect(\'' + str(succeeded) +'\', \'' + courseID + '\')"></body>')


db.commit()
db.close()
