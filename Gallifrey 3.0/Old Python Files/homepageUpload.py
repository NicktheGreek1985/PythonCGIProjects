#!/usr/bin/python
print('Content-type: text/html\n')

import cgi
import cgitb; cgitb.enable()
import os

form = cgi.FieldStorage()
fileitem = form['file_1']
fname = form.getvalue('filename')

fout = file (os.path.join('HomepageFiles', fileitem.filename), 'wb')

while 1:
    chunk = fileitem.file.read(100000)
    if not chunk: break
    fout.write(chunk)
fout.close()
print('<link rel="stylesheet" href="main.css" />')
print("<script src='script.js'></script>")
print('<body onload="addFile(\'' + fileitem.filename +'\',\'' + fname +'\')">')
print('<h1>Success!</h1>')
print('</body>')
