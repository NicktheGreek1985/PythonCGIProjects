#!/usr/bin/python
print 'Content-type: text/html'
print

# Import modules and set up database connection
import cgi
import cgitb; cgitb.enable()
import sqlite3

mydb = 'AstroHockey.db'
conn = sqlite3.connect(mydb)
cursor = conn.cursor()

print '<p><a href="PracTest.html">Return to main test page</a></p>'

#******************************************************
# THIS IS THE SECTION YOU WILL HAVE TO CHANGE
#

# Set up and execute SQL statement
cursor.execute('''SELECT SUM(suggested_deposit)
						FROM Equipment''')
records = cursor.fetchall()

#
#******************************************************

# Print out all the records that have been found in an HTML table
if len(records) > 0:
	print '<table border="1px solid black">'
	for record in records:
		print '<tr>'
		for field in record:
			print'<td>' + str(field) + '</td>'
		print '</tr>'
	print '</table>'
else:
	print 'No records found'
	
# Close the database connection
conn.commit()
cursor.close()
