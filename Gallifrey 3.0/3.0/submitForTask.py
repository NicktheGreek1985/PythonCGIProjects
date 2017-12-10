#!/usr/bin/python
print('Content-type: text/html\n')

import cgi
import cgitb; cgitb.enable()
import os

form = cgi.FieldStorage()

topic = form.getvalue('topic')
taskGroup = form.getvalue('taskgroup')
task = form.getvalue('task')

student = form.getvalue('student')

attachment = form['submission']
name = str(student) + '.' + str(topic) + '.' + str(taskGroup) + '.' + str(task) + attachment.filename

new_file = file(os.path.join('Submissions', name), 'wb')

while 1:
    chunk = attachment.file.read(100000)
    if not chunk:
        break
    new_file.write(chunk)
new_file.close()
print(topic, taskGroup, task, name)
print('<script src="script3.js"></script>')
print("<body onload='submitForTask(\""+ name +"\",\""+ topic +"\",\""+ taskGroup +"\",\""+ task +"\")\'><h1>Success!!</h1></body>")
