#!/usr/bin/python
print('Content-type: text/html\n')

import cgi
import cgitb; cgitb.enable()
import os

form = cgi.FieldStorage()
topic = form.getvalue('topic')
taskGroup = form.getvalue('taskgroup')
task = form.getvalue('task')

coverName = form.getvalue('attachmentName')
attachment = form['attachment']
name = str(topic) + '.' + str(taskGroup) + '.' + str(task) + attachment.filename

new_file = file(os.path.join('Attachments', name), 'wb')

while 1:
    chunk = attachment.file.read(100000)
    if not chunk:
        break
    new_file.write(chunk)
new_file.close()

print('<script src="script3.js"></script>')
print("<body onload='addAttachment(\""+ topic +'\",\"'+ taskGroup +'\",\"' +
      task +"\",\""+ coverName +"\",\""+ name +"\")\'><h1>Success!</h1></body>")
