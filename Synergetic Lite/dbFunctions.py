def print_Records(records, fields = None):
# Print out all the records that have been found in an HTML table
	if len(records) > 0:
		print('<table>')
		if fields != None:
			print('<tr>')
			for field in fields:
				print('<th><h3>' + str(field) + '</h3></th>')
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
		print('<h2>No records found</h2>')

def startHTML(title, stylesheet):
	print('<html>')
	print('<head>')
	print('<title>' + title + '</title>')
	print('<link rel="stylesheet" href="' + stylesheet + '.css">')
	print('<script src="script.js"></script>')
	print('</head>')
	print('<body>')
	print('<header><h3>Synergetic Lite</h3></header>')

def endHTML():
	print('<footer>Synergetic 1.0.0 <br>Created By Nick Patrikeos</footer>')
	print('</body>')
	print('</html>')
