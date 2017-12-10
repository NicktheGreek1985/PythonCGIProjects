import json

students = open('students.txt').read()
teachers = open('teacherout.txt').read().replace(' ', '')

f = open('final.json', 'w')
f.write(json.dumps([[], teachers, students, []]))
f.close()
