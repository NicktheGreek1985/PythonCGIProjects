#!/usr/bin/python
print('Content-type: text/html\n')

import cgi
import cgitb; cgitb.enable()
import json

storage = json.loads(open('output.txt').read())
print('<html>')
print('''<script>

StudentCourse = function(ref) {
    this.courseRef = ref
    this.progressUnmarked = 0
    this.progressCorrect = 0
    this.progressIncorrect = 0
    this.average = 0
    this.submissions = []
}

function displayData(data) {
	for (var i = 0; i < data.length; i++) {
		data[i].studentcourses = [new StudentCourse(data[i].classcode)]
	}
	document.getElementById('para').innerHTML = JSON.stringify(data)
}
</script>''')
print('<body onload=\'displayData(' + json.dumps(storage) + ')\'>')
print('<p id="para"></p>')
print('</body>')
print('</html>')
