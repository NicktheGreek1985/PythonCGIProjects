#!/usr/bin/python
print('Content-type: text/html\n')

'''

Synergetic Lite

editClass.py

Allows user to edit the details of Class ID, Teacher and Course for
an existing class.

Generates HTML (.py is required due to DB interaction)

By Nick Patrikeos on 19DEC17

'''

import cgi
import cgitb; cgitb.enable()
import sqlite3
from dbFunctions import *

def generateTeachersSelect(teachers, currentTeacher):
    returnStr = '<select name="teacherID">'

    for teacher in teachers:
        if teacher[0] == currentTeacher:
            returnStr += '<option value=' + teacher[0] + ' selected>' + teacher[0] + '</option>'
        else:
            returnStr += '<option value=' + teacher[0] + '>' + teacher[0] + '</option>'

    returnStr += '</select>'

    return returnStr

def generateCoursesSelect(courses, currentCourse):
    returnStr = '<select name="courseID" selected="' + currentCourse +'">'

    for course in courses:
        if course[0] == currentCourse:
            returnStr += '<option value=' + course[0] + ' selected>' + course[0] + '</option>'
        else:
            returnStr += '<option value=' + course[0] + '>' + course[0] + '</option>'

    returnStr += '</select>'

    return returnStr


form = cgi.FieldStorage()
oldClassID = form.getvalue('classID')

db = sqlite3.connect('synergetic.db')
cursor = db.cursor()
cursor.execute('PRAGMA foreign_keys = ON')

values = {'oldClassID':oldClassID}

t = cursor.execute('SELECT Teacher_ID FROM Teachers')
teachers = cursor.fetchall()
c = cursor.execute('SELECT Course_ID FROM Courses')
courses = cursor.fetchall()
cl = cursor.execute('SELECT * FROM Classes WHERE Class_ID = :oldClassID', values)
existingClass = cursor.fetchall()

startHTML('Synergetic Lite', 'main')


print('''<h1>Edit Class</h1>
        <hr>

        <div class='mainSection'>
            <div class='formContainer'>
                <form action='editClass2.py'>
                    <input type='text' name='oldClassID' value="''' +
                      oldClassID + '''" style='display: none;' />
                    <input type='text' name='newClassID' value="''' +
                      existingClass[0][0] +'''" /><br>
                    '''+ generateTeachersSelect(teachers, existingClass[0][1]) + '<br>' +
                      generateCoursesSelect(courses, existingClass[0][2]) + '''<br><input type='submit' />
                </form>
            </div>
        </div>
        <a href="classesManage.py"><div class="backButton">Back</div></a>
        <hr>
''')


endHTML()
