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

print('<h1>Multiple Continents</h1>')
print('<p>The following table lists the countries that are spread over more than one continent.</p>')

cursor.execute('SELECT Country.name, encompasses.continent FROM encompasses INNER JOIN Country WHERE encompasses.country = Country.code AND encompasses.percentage < 100')
records = cursor.fetchall()
fields = ['Country','Continent']
print_Records(records, fields)

endHTML()

cursor.close()
