#!/usr/bin/python
print('Content-type: text/html\n')

import cgitb; cgitb.enable()
import json

'''
students = json.dumps(json.loads(open('students.json').read())[0])
teachers = json.dumps(json.loads(open('students.json').read())[0])
classes = json.dumps(json.loads(open('students.json').read())[0])
topics = json.dumps(json.loads(open('students.json').read())[0])
courses = json.dumps(json.loads(open('students.json').read())[0])
'''
storage = json.loads(open('store3.json').read())
courses, teachers, students, classes, topics = storage[0], storage[1], storage[2], storage[3], storage[4]

print('<html>')
print('<head><script src="script3.js"></script>')
print('<body onload=\'setStoreToData(' + json.dumps(courses) + ',' + json.dumps(teachers) + ',' +
      json.dumps(students) + ','+ json.dumps(classes) + ',' + json.dumps(topics) +
      ');\'></body>')
print('</html>')
