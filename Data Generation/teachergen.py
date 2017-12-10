from random import choice, randint
import json
'''alpha = [ chr(x) for x in range(97, 97+26)]

names = ['Ben Lane', 'Max Shannon','Andrew Triglavcanin','Alex Brown', 'Ben Davison-Petch', 'Nick Patrikeos']
teachers = []
a = 0
for name in names:
    username = name[0].lower() + name.split()[1].lower()
    password = ''.join([ choice(alpha) for x in range(5) ]) + ''.join([ str(randint(0, 9)) for i in range(2)])
    classRefs = [a, a+6]
    studentRefs = [ [x for x in range(a*25, (a*25)+26)], [ y for y in range((a+6)*25, ((a+6)*25)+26)]]
    teachers.append({'name':name, 'username':username, 'password':password, 'classRefs':classRefs, 'studentRefs':studentRefs})
    a += 1
outfile = open('teacherout.txt','w')
outfile.write(json.dumps(teachers))
outfile.close()
'''

names = ['Ben Lane', 'Max Shannon','Andrew Triglavcanin','Alex Brown', 'Ben Davison-Petch', 'Nick Patrikeos']
classes = [{} for x in range(12)]

a = 0
for name in names:
    classes[a]['teacher'] = name
    classes[a+6]['teacher'] = name
    classes[a]['name'] = '07CSC' + str(a+1)
    classes[a+6]['name'] = '07CSC' + str(a+7)
    classes[a]['courseRef'] = 0
    classes[a+6]['courseRef'] = 0
    classes[a]['currentHomework'] = ""
    classes[a+6]['currentHomework'] = ""
    a += 1

outfile = open('classout.txt','w')
outfile.write(json.dumps(json.dumps(classes)))
outfile.close()
