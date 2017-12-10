def print_Records(records, fields = None):
# Print out all the records that have been found in an HTML table
	if len(records) > 0:
		print('<table>')
		if fields != None:
			print('<tr>')
			for field in fields:
				print('<th>' + str(field) + '</th>')
			print('</tr>')
		
		row = "rowA"
		for record in records:
			print('<tr class="' + row + '">')
			if row == "rowA":
				row = "rowB"
			else:
				row = "rowA"
			for field in record:
				print('<td>' + str(field) + '</td>')
			print('</tr>')
		print('</table>')
	else:
		print('No records found')
		
def startHTML(title, stylesheet):
	print('<html>')
	print('<head>')
	print('<title>' + title + '</title>')
	print('<link rel="stylesheet" href="' + stylesheet + '.css">')
	print('</head>')
	print('<body>')
	print('<p><a href="index.html">Return to Home Page</a></p>')

def endHTML():
	print('<p><a href="index.html">Return to Home Page</a></p>')
	print('</body>')
	print('</html>')

