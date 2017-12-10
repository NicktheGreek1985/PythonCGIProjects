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
language = form.getvalue('language')
values = { "language": language }

startHTML("Mondial Database", "stylesheet")
print('<h1>Information about ' + language + '</h1>')
print('<p>The following table lists some of the basic information about ' + language + '.</p>')

cursor.execute('''SELECT Country.name, Country.population, percentage FROM Language INNER JOIN Country WHERE Language.country = country.code AND
                Language.name = :language''', values)
records = cursor.fetchall()

fields = ["Name", "Population", "Percentage"]
print_Records(records, fields)
endHTML()

cursor.close()
