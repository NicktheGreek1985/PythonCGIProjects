#!/usr/bin/python
print('Content-type: text/html\n')

'''

Synergetic Lite

TEACHER SIDE

manageCourse.py

Creates HTML page to display all assessments for a course:
- name
- out of
- weighting
- Actions to edit, and delete

Also allows user to add a new assessment via link

By Nick Patrikeos on 02JAN18

'''

import cgi
import cgitb; cgitb.enable()
import sqlite3
from dbFunctions import *

db = sqlite3.connect('synergetic.db')
cursor = db.cursor()
cursor.execute('PRAGMA foreign_keys = ON')

form  = cgi.FieldStorage()
courseID = form.getvalue('courseID')
values = {'courseID': courseID}

cursor.execute('SELECT Assessment_ID, Name, Out_Of, Weighting FROM Assessments WHERE Course = :courseID', values)
records = cursor.fetchall()

startHTML('Synergetic Lite', 'main')

print('<h1>Course Management</h1>')

print('<a href="addAssessment.html"><div class="button" onclick="localStorage.setItem(\'currentCourse\', \'' + courseID + '\')">New Assessment</div></a>')

print('<hr>')

fieldnames = ['Name', 'Out Of', 'Weighting', 'Actions']

print('<div class="mainSection">')

for i in range(len(records)):
    if records[i][0] is not None:

        records[i] = (records[i][1], records[i][2], str(records[i][3]) + "%", '<form action="editAssessment.py" id="deleteForm"><input type="text" name="assessmentID" value="' +
        str(records[i][0]) + '" /><input type="submit" value="Edit"/></form> <form action="deleteAssessment.py" id="deleteForm"><input type="text" name="assessmentID" value="' +
        str(records[i][0]) + '" /><input type="submit" value="Delete"/></form>',)


print_Records(records, fields=fieldnames)
print('<div class="backButton" onclick="redirectToTeacherHomepage()">Back</div>')
print('</div>')

print('<hr>')

endHTML()
