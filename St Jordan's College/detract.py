#!/usr/bin/python
print('Content-type: text/html\n')

import cgi, cgitb; cgitb.enable()
from DB_Functions import *
from st_jordans_objects import *
import sqlite3

db = sqlite3.connect('students.db')
form = cgi.FieldStorage()
startHTML('St Jordan\'s College','stylesheet')

if form.getvalue('hod_username') in list([ str(x) for x in range(100, 121) ]) and form.getvalue('hod_password') == 'teachers123':
    for student in school:
        if int(form.getvalue('id')) == student.student_id:
            db.execute("UPDATE records SET Behaviours = '[" + form.getvalue('behaviour') + "]' WHERE Id = " + str(student.student_id) + ';')
    
            db.commit()
            print('<h1>Behaviour Recorded</h1>')
            student.behaviour_slips.append(form.getvalue('behaviour'))
            print(student.first_name + ' ' + student.surname + '\'s behaviours were changed.')
            break
else:
    print('<h1>Behaviour Recording Failed</h1>')
db.close()
endHTML()


