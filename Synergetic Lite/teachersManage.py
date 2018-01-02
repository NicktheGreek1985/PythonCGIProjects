#!/usr/bin/python
print('Content-type: text/html\n')

'''

Synergetic Lite

teachersManage.py

Creates HTML page to display all existing teachers, showing:
- ID
- Existing classes
- Actions to view timetable and remove teacher
in a table.

Also allows user to add a new teacher via link.

By Nick Patrikeos on 17DEC17

'''

import cgi
import cgitb; cgitb.enable()
import sqlite3
from dbFunctions import *

db = sqlite3.connect('synergetic.db')
cursor = db.cursor()
cursor.execute('PRAGMA foreign_keys = ON')

courses = cursor.execute('SELECT Teacher_ID, Is_Admin FROM Teachers')
records = cursor.fetchall()

startHTML('Synergetic Lite', 'main')

print('<h1>Teachers</h1>')

print('<a href="addTeacher.html"><div class="button">New Teacher</div></a>')

print('<hr>')

fieldnames = ['ID', 'Is Administrator', 'Classes', 'Actions']

print('<div class="mainSection">')

for i in range(len(records)):
    if records[i][0] is not None:
        cursor.execute('SELECT Class_ID FROM Classes WHERE Teacher = :teacherID', {'teacherID':records[i][0]})
        classes = ', '.join([ x[0] for x in cursor.fetchall() ])

        if records[i][1]:

            records[i] = (records[i][0], 'Yes', classes,
                          '<form action="viewTeacherTimetable.py" id="deleteForm"><input type="text" name="teacherID" value="' +
                           records[i][0] + '" /><input type="submit" value="Timetable"/></form> <form action="unmakeTeacherAdmin.py" id="deleteForm"><input type="text" name="teacherID" value="' +
                           records[i][0] + '" /><input type="submit" value="Unmake Admin"/></form> <form action="deleteTeacher.py" id="deleteForm"><input type="text" name="teacherID" value="' +
                           records[i][0] + '" /><input type="submit" value="Delete"/></form>',)
        else:
            records[i] = (records[i][0], 'No', classes,
                          '<form action="viewTeacherTimetable.py" id="deleteForm"><input type="text" name="teacherID" value="' +
                           records[i][0] + '" /><input type="submit" value="Timetable"/></form> <form action="makeTeacherAdmin.py" id="deleteForm"><input type="text" name="teacherID" value="' +
                           records[i][0] + '" /><input type="submit" value="Make Admin"/></form> <form action="deleteTeacher.py" id="deleteForm"><input type="text" name="teacherID" value="' +
                           records[i][0] + '" /><input type="submit" value="Delete"/></form>',)


print_Records(records, fields=fieldnames)
print('<a href="adminHomepage.html"><div class="backButton">Back</div></a>')
print('</div>')

print('<hr>')

endHTML()
