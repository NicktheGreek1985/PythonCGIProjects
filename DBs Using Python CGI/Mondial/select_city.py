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
city = form.getvalue('city')
values = { "city": city }

startHTML("Mondial Database", "stylesheet")
print('<h1>Information about ' + city + '</h1>')
print('<p>The following table lists some of the basic information about ' + city + '.</p>')

cursor.execute('''SELECT * FROM City
                   WHERE name = :city''', values)
records = cursor.fetchall()

fields = ["Name", "Country", "Province", "Population", "Elevation",'Coordinates']
print_Records(records, fields)
endHTML()

cursor.close()
