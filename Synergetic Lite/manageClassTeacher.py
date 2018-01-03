#!/usr/bin/python
print('Content-type: text/html\n')

'''

Synergetic Lite

TEACHER SIDE

manageClass.py

Allows the user to view the details for a class as well as the students enrolled.
Allows the user to add and remove students from the class.

By Nick Patrikeos on 19DEC17

'''

import cgi
import cgitb; cgitb.enable()
import sqlite3
from dbFunctions import *

form = cgi.FieldStorage()
classID = form.getvalue('classID')
values = {'classID':classID}

db = sqlite3.connect('synergetic.db')
cursor = db.cursor()
cursor.execute('PRAGMA foreign_keys = ON')

cursor.execute('SELECT * FROM Classes WHERE Class_ID = :classID',values)
records = cursor.fetchall()

startHTML('Synergetic Lite', 'main')

print('<h1>Class Management</h1>')

print('<hr>')
print('<div class="mainSection">')
print('<p>Class ID</p>')
print('<h3>' + records[0][0] + '</h3>')
print('<p>Teacher</p>')
print('<h3>' + records[0][1] + '</h3>')
print('<p>Course</p>')
print('<h3>' + records[0][2] + '</h3>')
print('<hr>')

fieldnames = ['ID','Actions']
cursor.execute('SELECT Student FROM Enrolments WHERE Class = :classID', values)
records = cursor.fetchall()
'''
for i in range(len(records)):
    if records[i][0] is not None:
        records[i] += ('<form action="deleteEnrolment.py" id="deleteForm"><input type="text" name="studentID" value="' +
                       str(records[i][0]) + '" /><input type="text" name="classID" value="' + classID + '" /><input type="submit" value="Remove"/></form>',)
'''

print_Records(records, fields=fieldnames)
print('<div class="backButton" onclick="redirectToTeacherHomepage()">Back</div>')
print('</div>')

print('<hr>')

endHTML()
