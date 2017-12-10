#!/usr/bin/python
print('Content-type: text/html\n')

import cgi
import cgitb; cgitb.enable()
import json

form = cgi.FieldStorage()
courses = form.getvalue('courses')
teachers = form.getvalue('teachers')
students = form.getvalue('students')
classes = form.getvalue('classes')
topics = form.getvalue('topics')

location = form.getvalue('location')

store = open('store3.json', 'w')
store.truncate()
store.write(json.dumps([courses, teachers, students, classes, topics]))
store.close()

print('<html>')
print("<script src='script3.js'></script>")
print('<body onload="redirectToLocation(\'' + location + '\')">')
print('</body>')
print('</html>')
