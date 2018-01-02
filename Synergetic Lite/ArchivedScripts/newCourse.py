#!/usr/bin/python
print('Content-type: text/html\n')

'''

Synergetic Lite

newCourse.py

Creates HTML page allow the user to add a new course.

By Nick Patrikeos on 15DEC17

'''

import cgi
import cgitb; cgitb.enable()
import sqlite3
from dbFunctions import *

db = sqlite3.connect('synergetic.db')
cursor = db.cursor()

courses = cursor.execute('SELECT * FROM Courses')
records = cursor.fetchall()

startHTML('Synergetic Lite', 'main')

print('''<h1>New Course</h1>
        <hr>
        <div class='mainSection'>
            <div class='formContainer'>
                <form action='addCourse.py'>
                    <input type='text' name='courseID' placeholder='Course ID'/><br>
                    <input type='submit' />
                </form>
            </div>
        </div>
        <hr>''')

endHTML()
