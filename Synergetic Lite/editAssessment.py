#!/usr/bin/python
print('Content-type: text/html\n')

'''

Synergetic Lite

editAssessment.py

Allows user to edit the details of Name, out of and weighting for an assessment

Generates HTML (.py is required due to DB interaction)

By Nick Patrikeos on 02JAN18

'''

import cgi
import cgitb; cgitb.enable()
import sqlite3
from dbFunctions import *

form = cgi.FieldStorage()
assessmentID = form.getvalue('assessmentID')
values = {'assessmentID':assessmentID}

db = sqlite3.connect('synergetic.db')
cursor = db.cursor()
cursor.execute('PRAGMA foreign_keys = ON')

cursor.execute('SELECT Name, Out_Of, Weighting FROM Assessments WHERE Assessment_ID = :assessmentID', values)
records = cursor.fetchall()

assessmentName = records[0][0]
outOf = records[0][1]
weighting = records[0][2]

startHTML('Synergetic Lite', 'main')

print('''
        <h1>Edit Assessment</h1>
        <hr>

        <div class='mainSection'>
            <div class='formContainer'>
                <form action='editAssessment2.py'>
                    <input type='text' name='assessmentID' style="display: none" value="''' + assessmentID + '''"/>
                    <input type='text' name='assessmentName' value="''' + assessmentName + '''"/><br>
                    <input type='text' name='outOf' value="''' + str(outOf) + '''"/><br>
                    <input type='text' name='weighting' value="''' + str(weighting) + '''"/><br>
                    <input type='submit' />
                </form>
            </div>
        </div>

        <hr>
''')

endHTML()
