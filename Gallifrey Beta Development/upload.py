#!/usr/bin/python
print('Content-type: text/html\n')

import cgi
import cgitb; cgitb.enable()
import os


form = cgi.FieldStorage()
unit = form.getvalue('unit')
module = form.getvalue('module')
activity = form.getvalue('activity')
fileitem = form['file_1']#form.getvalue('file_1')
fname = form.getvalue('filename')
fileitem.filename = fname
filename = fname

fout = file (os.path.join('Attachments', fileitem.filename), 'wb')
while 1:
    chunk = fileitem.file.read(100000)
    if not chunk: break
    fout.write (chunk)
fout.close()
print('<link rel="stylesheet" href="main.css" />')
print("<script src='script.js'></script>")
print("<body onload='changeActivityAttachment(\""+unit+'\",\"'+module+'\",\"'+activity+"\",\""+filename+"\")\'>")

print('<h1>Success!</h1>')
print('</body>')
