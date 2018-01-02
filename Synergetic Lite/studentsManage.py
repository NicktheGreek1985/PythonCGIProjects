#!/usr/bin/python
print('Content-type: text/html\n')

'''

Synergetic Lite

studentsManage.py

Creates HTML page to display all existing students, showing:
- Student ID
- Actions view timetable and remove teacher
in a table.

Also allows user to add a new student via link.

By Nick Patrikeos on 19DEC17

'''

import cgi
import cgitb; cgitb.enable()
import sqlite3
from dbFunctions import *

db = sqlite3.connect('synergetic.db')
cursor = db.cursor()
cursor.execute('PRAGMA foreign_keys = ON')

courses = cursor.execute('SELECT Student_ID FROM Students')
records = cursor.fetchall()

startHTML('Synergetic Lite', 'main')

print('<h1>Students</h1>')

print('<a href="addStudent.html"><div class="button">New Student</div></a>')

print('<hr>')

fieldnames = ['ID','Classes','Actions']

print('<div class="mainSection">')

for i in range(len(records)):
    if records[i][0] is not None:
        cursor.execute('SELECT Class FROM Enrolments WHERE Student = :studentID', {'studentID':records[i][0]})
        classes = ', '.join([ x[0] for x in cursor.fetchall() ])

        records[i] += (classes, ' <form action="viewStudentTimetable.py" id="deleteForm"><input type="text" name="studentID" value="' +
        str(records[i][0]) + '" /><input type="submit" value="Timetable"/></form> <form action="deleteStudent.py" id="deleteForm"><input type="text" name="studentID" value="' +
                       str(records[i][0]) + '" /><input type="submit" value="Delete"/></form>',)


print_Records(records, fields=fieldnames)
print('<a href="adminHomepage.html"><div class="backButton">Back</div></a>')
print('</div>')

print('<hr>')

endHTML()
