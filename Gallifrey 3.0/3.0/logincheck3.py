#!/usr/bin/python
print('Content-type: text/html\n')

import cgi
import cgitb; cgitb.enable()
import json
import hashlib

form = cgi.FieldStorage()
username = form.getvalue('username')
password = form.getvalue('password')
'''
storage = json.loads(open('store3.json').read())

students = [ i for i in json.loads(storage[2]) ]
teachers = [ i for i in json.loads(storage[1]) ]
'''
students = [ json.loads(i) for i in json.loads(open('students.json').read()) ]
teachers = [ json.loads(i) for i in json.loads(open('teachers.json').read()) ]

x = hashlib.sha224()
x.update(password)
hashedpass = x.hexdigest()
# print(hashedpass)
def verify():
    for student in students:
        print(student['password'])
        try:
            if student['id'] == int(username) and student['password'] == hashedpass:
                return ('student', student['id'])
        except: pass
    
    for teacher in teachers:
        if teacher['username'] == username and teacher['password'] == hashedpass:
            return ('teacher', teacher['username'])
    return False

print('<html>')

# print('<link rel="stylesheet" href="main.css" />')
print("<script src='script3.js'></script>")
print('<title>Gallifrey</title>')

verification = verify()
# print(verification)
if verification:
    if verification[0] == 'student':
        print('<body onload="setupStudentLogin(' + str(verification[1]) + ')">')
    elif verification[0] == 'teacher':
        print('<body onload="setupTeacherLogin(\'' + str(verification[1]) + '\')">')
    print('</body></html>')
else:
    print('<body onload="handleFailedLogin()"></body></html>')
