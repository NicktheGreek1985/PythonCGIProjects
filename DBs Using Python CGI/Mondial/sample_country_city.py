#!/usr/bin/python
print 'Content-type: text/html'
print

import cgi
import cgitb; cgitb.enable()
import sqlite3
from DB_Functions import *

mydb = 'mondial.db'
conn = sqlite3.connect(mydb)
cursor = conn.cursor()

#####
# Retrieve the search values from the HTML form
form = cgi.FieldStorage()
#
# Add the values from the form to a dictionary
country = form.getvalue('country')
values = { "country": country }
#
#####

#####
# Start building the HTML for the results of your database query
#
# Add the title and the name of the CSS stylesheet as parameters
#
startHTML("Mondial Database", "stylesheet")
#
# Add a heading to your results page
print('<h1>Cities of ' + country + '</h1>')
print('<p>The following table lists some of the main cities of ' + country + '. The cities are listed in order of population size.</p>')
#
#####

#####
#
# Build your SQL query here for the program to execute.
# NOTE: Use the values in the dictionary to build your search
#
cursor.execute('''SELECT City.name, City.province, City.population FROM City
                    INNER JOIN Country
                    WHERE City.country = Country.code
                    AND   Country.name = :country
                    ORDER BY City.population DESC''', values)
records = cursor.fetchall()
#
#####

#####
#
# Build the rest of the HTML to show your results.
#
# Add the field names to use as table headings
fields = ["Name", "Province", "Population"]
#
# Build the HTML table with the results from the database query
print_Records(records, fields)
#
# Add the end of the HTML
endHTML()

cursor.close()