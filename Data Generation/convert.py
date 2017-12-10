from names import Names
from random import randint, choice
from json import dumps

students = []
alpha = [ chr(x) for x in range(97, 97+26)]
x = 0
y = 0

done = []

def getStudentId():
    i = randint(1010000, 1019999)
    if i in done:
        getStudentId()
    done.append(i)
    return i

for name in Names:
    f, l = name.split()[0], name.split()[1]
    password = ''.join([ choice(alpha) for i in range(5) ]) + ''.join([str(randint(0, 9)) for j in range(2)])
    studentid = getStudentId()
    students.append({'firstname': f, 'lastname': l, 'password': password, 'id': studentid, 'classcode': x})
    y += 1
    if y > 25:
        x += 1
        y = 0


outfile = open('output.txt','w')
outfile.write(dumps(students))
