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

print('<h1>The Kalahari Desert</h1>')
print('<p>The following table lists the countries which the Kalahari desert is part of.</p>')

cursor.execute('SELECT Country.name, geo_desert.desert FROM geo_desert INNER JOIN Country WHERE geo_desert.country = Country.code AND geo_desert.desert = "Kalahari"')
records = cursor.fetchall()
fields = ['Country','Desert']
print_Records(records, fields)

endHTML()

cursor.close()
