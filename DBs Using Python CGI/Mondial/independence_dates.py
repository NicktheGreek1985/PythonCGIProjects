#!/usr/bin/python
print('Content-type: text/html\n')

import cgi
import cgitb; cgitb.enable()
import sqlite3
from DB_Functions import *

mydb = 'mondial.db'
conn = sqlite3.connect(mydb)
cursor = conn.cursor()

startHTML('Mondial Database', 'stylesheet')

print('<h1>Independence Day</h1>')
print('<p>The following table lists the independence day of the countries.</p>')

cursor.execute('SELECT Country.name, independence FROM Politics INNER JOIN Country WHERE Politics.country = Country.code')
records = cursor.fetchall()
fields = ['Country','Independence Date']
print_Records(records, fields)

endHTML()

cursor.close()
