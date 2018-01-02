#!/usr/bin/python
print('Content-type: text/html\n')

'''

Synergetic Lite

classesManage.py

Creates HTML page to display all existing classes, showing:
- ID
- Course
- Teacher
- Actions to manage, edit, view timetable and delete class
in a table.

Also allows user to add a new class via link.

By Nick Patrikeos on 16DEC17

'''

import cgi
import cgitb; cgitb.enable()
import sqlite3
from dbFunctions import *

db = sqlite3.connect('synergetic.db')
cursor = db.cursor()
cursor.execute('PRAGMA foreign_keys = ON')

courses = cursor.execute('SELECT * FROM Classes')
records = cursor.fetchall()

startHTML('Synergetic Lite', 'main')

print('<h1>Classes</h1>')

print('<a href="addClass.py"><div class="button">New Class</div></a>')

print('<hr>')

fieldnames = ['ID', 'Teacher', 'Course', 'Actions']

print('<div class="mainSection">')

for i in range(len(records)):
    if records[i][0] is not None:
        records[i] += ('<form action="manageClass.py" id="deleteForm"><input type="text" name="classID" value="' +
                       records[i][0] + '" /><input type="submit" value="Manage"/></form> <form action="manageClassTimetable.py" id="deleteForm"><input type="text" name="classID" value="' +
                       records[i][0] + '" /><input type="submit" value="Timetable"/></form> <form action="editClass.py" id="deleteForm"><input type="text" name="classID" value="' +
                       records[i][0] + '" /><input type="submit" value="Edit"/></form> <form action="deleteClass.py" id="deleteForm"><input type="text" name="classID" value="' +
                       records[i][0] + '" /><input type="submit" value="Delete"/></form>',)


print_Records(records, fields=fieldnames)
print('<a href="adminHomepage.html"><div class="backButton">Back</div></a>')
print('</div>')

print('<hr>')

endHTML()
