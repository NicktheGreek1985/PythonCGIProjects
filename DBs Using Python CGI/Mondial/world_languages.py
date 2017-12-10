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

print('<h1>Languages of the World</h1>')
print('<p>The following table lists the languages that are spoken by more than 80% of the population of a country.</p>')

cursor.execute('SELECT Country.name, Language.name, Language.percentage FROM Language INNER JOIN Country WHERE Language.country = Country.code AND Language.percentage > 80')
records = cursor.fetchall()
fields = ['Country','Language','Percentage']
print_Records(records, fields)

endHTML()

cursor.close()
