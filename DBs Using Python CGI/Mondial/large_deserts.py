#!/usr/bin/python
print('Content-type: text/html\n')


import cgi
import cgitb; cgitb.enable()
import sqlite3

from DB_Functions import *

mydb = 'mondial.db'
conn = sqlite3.connect(mydb)
cursor = conn.cursor()

#####
# Start building the HTML for the results of your database query
#
# Add the title and the name of the CSS stylesheet as parameters
#
startHTML("Mondial Database", "stylesheet")
#
# Add a heading to your results page
#
print('<h1>Large Deserts</h1>')
print('<p>The following table lists the 5 largest deserts.</p>')
#
#####

#####
#
# Build your SQL query here for the program to execute
#
cursor.execute('SELECT name, area FROM Desert ORDER BY area DESC LIMIT 5')
records = cursor.fetchall()

#my_data = list(cursor.execute('SELECT * FROM Country'))
#for i in my_data:
#    print(i)
#
#####

#####
#
# Build the rest of the HTML to show your results.
#
# Add the field names to use as table headings
fields = ["Name", 'Area']
#
# Build the HTML table with the results from the database query
print_Records(records, fields)
#
# Add the end of the HTML
endHTML()

cursor.close()
