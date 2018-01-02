#!/usr/bin/python
print('Content-type: text/html\n')

'''

Synergetic Lite

coursesManage.py

Creates HTML page to display all existing courses, showing:
- ID
- Existing classes
- Actions to view timetable and delete course
in a table.

Also allows user to add a new course via link.

By Nick Patrikeos on 14DEC17

'''

import cgi
import cgitb; cgitb.enable()
import sqlite3
from dbFunctions import *

db = sqlite3.connect('synergetic.db')
cursor = db.cursor()
cursor.execute('PRAGMA foreign_keys = ON')

courses = cursor.execute('SELECT * FROM Courses')
records = cursor.fetchall()

startHTML('Synergetic Lite', 'main')

print('<h1>Courses</h1>')

print('<a href="addCourse.html"><div class="button">New Course</div></a>')

print('<hr>')

fieldnames = ['ID', 'Classes', 'Actions']

print('<div class="mainSection">')

for i in range(len(records)):
    if records[i][0] is not None:
        cursor.execute('SELECT Class_ID FROM Classes WHERE Course = :courseID', {'courseID':records[i][0]})
        classes = ', '.join([ x[0] for x in cursor.fetchall() ])

        records[i] += (classes, '<a href="editCourse.html" onclick="setCurrentCourse(\'' +
                       records[i][0] + '\')">Edit</a> <form action="deleteCourse.py" id="deleteForm"><input type="text" name="courseID" value="' +
                       records[i][0] + '" /><input type="submit" value="Delete"/></form>',)


print_Records(records, fields=fieldnames)
print('<a href="adminHomepage.html"><div class="backButton">Back</div></a>')
print('</div>')

print('<hr>')

endHTML()
