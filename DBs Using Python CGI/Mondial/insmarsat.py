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

print('<h1>International Mobile Satellite Organization</h1>')
print('<p>The following table lists the countries in the IMSO, their population and their membership types</p>')

cursor.execute('SELECT Country.name, Country.population, isMember.type FROM isMember INNER JOIN Organization INNER JOIN Country WHERE isMember.Organization = Organization.abbreviation AND isMember.country = Country.code AND Organization.name = "International Mobile Satellite Organization"')
records = cursor.fetchall()
fields = ['Name','Population','Type of Membership']
print_Records(records, fields)

endHTML()

cursor.close()
