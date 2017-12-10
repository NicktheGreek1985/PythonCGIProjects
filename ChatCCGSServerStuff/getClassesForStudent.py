#!/usr/bin/python
print('Content-type: text/plain\n')

import sqlite3
import cgi

conn = sqlite3.connect('test.db')

form = cgi.FieldStorage()

requiredFields = ["username"]
inp = {'username':None}


if not all([x in form for x in requiredFields]):
    print("400 Bad Request")
    exit()

try:
    inp["username"] = form["username"].value
    # print(inp)
    
except:
    print("422 Unprocessable Entity")
    exit()

try:
    data = conn.execute('SELECT classID FROM Enrolments WHERE studentID = {}'.format(inp['username']))
except Exception as e:
    print("Internal server error.", e)
    exit()

for d in data:
    print(d[0])
