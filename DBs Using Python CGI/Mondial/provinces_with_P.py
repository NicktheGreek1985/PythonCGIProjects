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

print('<h1>Provinces in P</h1>')
print('<p>The following table lists all the provinces in countries that start with the letter P, but only if there is more than one province in that country.</p>')

cursor.execute('SELECT Country.name, Country.population, Country.area, Province.capital FROM Province INNER JOIN Country WHERE Province.country = Country.code AND Province.area < Country.area AND Country.name LIKE "P%"')
records = cursor.fetchall()
fields = ['Name','Population','Area','Capital']
print_Records(records, fields)

endHTML()

cursor.close()
