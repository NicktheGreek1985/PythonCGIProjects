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

print('<h1>Cities by Country</h1>')
print('<p>The following table lists the cities for each country.</p>')

cursor.execute('SELECT City.name, code from City INNER JOIN Country WHERE City.country = Country.code')
records = cursor.fetchall()
fields = ['City','Country']
print_Records(records, fields)

endHTML()

cursor.close()
