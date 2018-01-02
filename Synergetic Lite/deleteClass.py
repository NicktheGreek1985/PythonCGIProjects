#!/usr/bin/python
print('Content-type: text/html\n')

'''

Synergetic Lite

deleteClass.py

Deletes a class from the DB.

By Nick Patrikeos on 19DEC17

'''

import cgi
import cgitb; cgitb.enable()
import sqlite3
from dbFunctions import *

db = sqlite3.connect('synergetic.db')
cursor = db.cursor()
cursor.execute('PRAGMA foreign_keys = ON')

form = cgi.FieldStorage()

classID = form.getvalue('classID')
values = {'classID':classID}

print('<script src="script.js"></script>')

cursor.execute('DELETE FROM Classes WHERE Class_ID = :classID', values)

print('<body onload=\'classesRedirect(2)\'></body>')

db.commit()
db.close()
