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

print('<h1>Countries in Europe</h1>')
print('<p>The following table lists the countries in Europe ordered by population descending.</p>')

cursor.execute('SELECT Country.name, Country.population FROM encompasses INNER JOIN Country INNER JOIN Continent WHERE encompasses.Continent = Continent.name AND encompasses.country = Country.code AND continent.name = "Europe" ORDER BY Country.population DESC')
records = cursor.fetchall()
fields = ['Name','Population']
print_Records(records, fields)

endHTML()

cursor.close()
