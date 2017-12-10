#!/usr/bin/python
print 'Content-type: text/html'
print

import cgi
import cgitb; cgitb.enable()
import sqlite3
from DB_Functions import *

mydb = 'mondial.db'
conn = sqlite3.connect(mydb)
cursor = conn.cursor()

form = cgi.FieldStorage()
mountain = form.getvalue('mountain')
values = { "mountain": mountain }

startHTML("Mondial Database", "stylesheet")
print('<h1>Information about ' + mountain + '</h1>')
print('<p>The following table lists some of the basic information about ' + mountain + '.</p>')

cursor.execute('''SELECT * FROM Mountain
                   WHERE name = :mountain''', values)
records = cursor.fetchall()

fields = ["Name", "Mountains", "Elevation", "Type", "Longitude", "Latitude"]
print_Records(records, fields)
endHTML()

cursor.close()
