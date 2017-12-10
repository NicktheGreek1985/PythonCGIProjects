#!/usr/bin/python
print('Content-type: text/html\n')

import json
import cgi
import cgitb; cgitb.enable()

form = cgi.FieldStorage()
courses = form.getvalue('courses')
teachers = form.getvalue('teachers')
users = form.getvalue('users')
classes = form.getvalue('classes')

store = open('store.json', 'w')
store.truncate()
store.write(json.dumps([courses, teachers, users, classes]))
store.close()
print('<html>')
print('<link rel="stylesheet" href="main.css" />')
print("<script src='script.js'></script>")
print('<body onload="redr()">')
print('<h1>Thank you for using Gallifrey.</h1>')
print('</body>')
print('</html>')
