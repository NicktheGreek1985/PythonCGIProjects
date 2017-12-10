import sqlite3
from st_jordans_objects import *

db = sqlite3.connect('students.db')

db.execute('DROP TABLE IF EXISTS records')
db.execute('CREATE TABLE records (Id INT, Firstname TEXT, Surname TEXT, Behaviours TEXT)')

for student in s():
    db.execute('INSERT INTO records (Id, Firstname, Surname) VALUES(?, ?, ?)', (student.student_id, student.first_name, student.surname))

db.commit()
db.close()
