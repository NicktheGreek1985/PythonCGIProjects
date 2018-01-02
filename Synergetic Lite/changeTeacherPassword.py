#!/usr/bin/python
print('Content-type: text/html\n')

'''

Synergetic Lite

changeTeacherPassword.py

Provided the old password is correct and thew new and verify passwords match,
changes the password for a teacher

By Nick Patrikeos on 02JAN18

'''

import cgi
import cgitb; cgitb.enable()
import sqlite3
from dbFunctions import *

db = sqlite3.connect('synergetic.db')
cursor = db.cursor()
cursor.execute('PRAGMA foreign_keys = ON')

form = cgi.FieldStorage()

oldPassword = form.getvalue('oldPassword')
newPassword = form.getvalue('newPassword')
verifyPassword = form.getvalue('verifyPassword')
teacherID = form.getvalue('teacherID')

values = {'oldPassword':oldPassword, 'newPassword':newPassword,
         'verifyPassword':verifyPassword, 'teacherID':teacherID}

print('<script src="script.js"></script>')

cursor.execute('SELECT Password FROM Teachers WHERE Teacher_ID = :teacherID', values)
currentPassword = cursor.fetchall()[0][0]

if oldPassword != currentPassword:
    print('<body onload="passwordRedirect(0)"></body>')
elif newPassword != verifyPassword:
    print('<body onload="passwordRedirect(1)"></body>')
else:
    ## :)
    cursor.execute('UPDATE Teachers SET Password = :newPassword WHERE Teacher_ID = :teacherID', values)
    print('<body onload="passwordRedirect(2)"></body>')

db.commit()
db.close()
