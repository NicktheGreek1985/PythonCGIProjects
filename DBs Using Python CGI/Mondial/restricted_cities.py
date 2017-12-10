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

print('<h1>Restricted Cities</h1>')
print('<p>The following table lists the name of the country and the name, province and population for each city.</p>')

cursor.execute('SELECT City.name, Country.name, City.province, City.population from City INNER JOIN Country WHERE City.country = Country.code')
records = cursor.fetchall()
fields = ['City','Country','Province','Population']
print_Records(records, fields)

endHTML()

cursor.close()
