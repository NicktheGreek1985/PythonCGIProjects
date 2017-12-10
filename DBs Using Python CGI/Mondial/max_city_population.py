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

print('<h1>Maximum Populations</h1>')
print('<p>The following table lists the cities that have the highest populations</p>')

cursor.execute('SELECT Country.name, City.name, City.population FROM City INNER JOIN Country WHERE City.country = Country.code')
records = cursor.fetchall()

fields = ['Country','City','Population']
print_Records(records, fields)

endHTML()

cursor.close()
