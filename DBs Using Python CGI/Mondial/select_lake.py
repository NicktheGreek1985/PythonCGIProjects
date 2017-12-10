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
lake = form.getvalue('lake')
values = { "lake": lake }

startHTML("Mondial Database", "stylesheet")
print('<h1>Information about ' + lake + '</h1>')
print('<p>The following table lists some of the basic information about ' + lake + '.</p>')

cursor.execute('''SELECT * FROM Lake
                   WHERE name = :lake''', values)
records = cursor.fetchall()

fields = ["Name", "Area", "Depth", "Elevation", "Type", "River",'Longitude','Latitude']
print_Records(records, fields)
endHTML()

cursor.close()
