#!/usr/bin/python
print('Content-type: text/html\n')

import cgi, cgitb; cgitb.enable()
from DB_Functions import *
from st_jordans_objects import *
import sqlite3

db = sqlite3.connect('students.db')
db = db.cursor()

form = cgi.FieldStorage()

if form.getvalue('username') in list([ str(x) for x in range(100, 121) ]) and form.getvalue('password') == 'password':
    teacher_valid = True
    HOD_valid = True
elif form.getvalue('username') in list([ str(x) for x in range(100, 121) ]) and form.getvalue('password') == 'teachers123':
    teacher_valid = False
    HOD_valid = True
else:
    teacher_valid = False
    HOD_valid = False

 
startHTML('St Jordan\'s College', 'stylesheet')

if teacher_valid or HOD_valid:
    print('<h1>St Jordan\'s College</h1>')
    db.execute('SELECT * FROM records')
    data = db.fetchall()
    print_Records(data, ['ID','First Name','Surname', 'Most Recent Behaviour'])
    print("<div class='behaviour_button'><a href='detract.html'>Add Behaviour</a></div>")
else:
    print('<h1>Login Failed</h1>')

endHTML()
