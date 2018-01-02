#!/usr/bin/python
print('Content-type: text/html\n')

'''

Synergetic Lite

verifyLogin.py

Verifies the username and password in the database to ensure user is
an existing student, teacher or parent. If verified, redirects the user
to their correct interface. If not, redirects the user to the login page

By Nick Patrikeos on 13DEC17

'''

import cgi
import cgitb; cgitb.enable()
import sqlite3

form = cgi.FieldStorage()

username = form.getvalue('username')
password = form.getvalue('password')

db = sqlite3.connect('synergetic.db')
cursor = db.cursor()
cursor.execute('PRAGMA foreign_keys = ON')

values = {'username':username, 'password':password}
# print(values)
print('<script src="script.js"></script>')

def verifyAndRedirect():
    isStudent = cursor.execute('SELECT * FROM Students WHERE Student_ID = :username AND Password = :password', values)
    records = cursor.fetchall()

    if records:
        print('<body onload="redirectOnLogin(\'student\', ' + username + ')"></body>')
        # Log in as student
        return

    isTeacher = cursor.execute('SELECT * FROM Teachers WHERE Teacher_ID = :username AND Password = :password', values)
    records = cursor.fetchall()

    if records:
        # Log in as teacher or admin
        isAdmin = records[0][2]
        if isAdmin:
            print('<body onload="redirectOnLogin(\'admin\', \'' + username + '\')"></body>')
            # Log in as admin
            return
        else:
            print('<body onload="redirectOnLogin(\'teacher\', \'' + username + '\')"></body>')
            # Log in as teacher
            return

    isParent = cursor.execute('SELECT * FROM Parents WHERE Parent_ID = :username AND Password = :password',values)
    records = cursor.fetchall()

    if records:
        print('<body onload="redirectOnLogin(\'parent\', ' + username + ')"></body>')
        # Log in as parent
        return

    print('<body onload="redirectOnLogin(\'failedLogin\', \'' + username + '\')"></body>')
verifyAndRedirect()
