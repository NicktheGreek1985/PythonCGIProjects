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

print('<h1>Twenty five Provinces</h1>')
print('<p>The following table lists the countries that have 25 provinces.</p>')

cursor.execute('SELECT Country.name, Country.population, Country.area FROM Province INNER JOIN Country WHERE Province.country = Country.code AND Province.area < Country.area')
records = cursor.fetchall()

fields = ['Name','Population','Area']
print_Records(records, fields)

endHTML()

cursor.close()
