#!/usr/bin/python
print('Content-type: text/html\n')

'''

Synergetic Lite

addClass.py

Allows user to add a new class, detailing Class ID, Course and Teacher

Generates HTML (.py is required due to DB interaction)

By Nick Patrikeos on 19DEC17

'''

import cgi
import cgitb; cgitb.enable()
import sqlite3
from dbFunctions import *

def generateTeachersSelect(teachers):
    returnStr = '<select name="teacherID">'

    for teacher in teachers:
        returnStr += '<option value=' + teacher[0] + '>' + teacher[0] + '</option>'

    returnStr += '</select>'

    return returnStr

def generateCoursesSelect(courses):
    returnStr = '<select name="courseID">'

    for course in courses:
        returnStr += '<option value=' + course[0] + '>' + course[0] + '</option>'

    returnStr += '</select>'

    return returnStr

db = sqlite3.connect('synergetic.db')
cursor = db.cursor()
cursor.execute('PRAGMA foreign_keys = ON')

t = cursor.execute('SELECT Teacher_ID FROM Teachers')
teachers = cursor.fetchall()
c = cursor.execute('SELECT Course_ID FROM Courses')
courses = cursor.fetchall()

startHTML('Synergetic Lite', 'main')


print('''<h1>New Class</h1>
        <hr>

        <div class='mainSection'>
            <div class='formContainer'>
                <form action='addClass2.py'>
                    <input type='text' name='classID' placeholder='Class ID'/><br>
                    '''+ generateTeachersSelect(teachers) + '<br>' +
                      generateCoursesSelect(courses) + '''<br><input type='submit' />
                </form>
            </div>
        </div>

        <hr>
''')


endHTML()
