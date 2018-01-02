#!/usr/bin/python
print('Content-type: text/html\n')

'''

Synergetic Lite

viewTeacherTimetable.py

Creates HTML page to display the timetable for a teacher.

By Nick Patrikeos on 24DEC17

'''

import cgi
import cgitb; cgitb.enable()
import sqlite3
from dbFunctions import *

def print_Timetable(t):
    # Prints out the periods in correct order
    # t is a single ordered array containing all periods a student has
    timetable = []
    for period in range(30):

        cl = -1
        for i in t:
            if period == i[0]:
                cl = i[1] + ' : ' + i[2]

        if period in [28, 29,18]:
            timetable.append(('', 0))
        elif cl != -1:
            timetable.append((cl,1))
        else:
            timetable.append(('', 2))

    print('<table>')
    print('<tr>')

    for field in  ['Monday','Tuesday','Wednesday','Thursday','Friday']:
        print('<th><h3>' + field + '</h3></th>')
    print('</tr>')

    order = [ [0, 6, 12, 18, 24],
    [1, 7, 13, 19, 25],
    [2, 8, 14, 20, 26],
    [3, 9, 15, 21, 27],
    [4, 10, 16, 22, 28],
    [5, 11, 17, 23, 29]]

    alt = 'rowA'
    for row in order:
        print('<tr class="' + alt + '">')

        if alt == "rowA":
            alt = "rowB"
        else:
            alt = "rowA"

        for col in row:
            if timetable[col][1] == 0:
                print('<td style="background-color: rgb(45, 136, 205)">' + str((col+1)%6 if (col+1)%6 != 0 else 6) +' '+ '' + '</td>')
            elif timetable[col][1] == 1:
                print('<td>' + str((col+1)%6 if (col+1)%6 != 0 else 6) +' '+ timetable[col][0] + '</td>')
            elif timetable[col][1] == 2:
                print('<td>' + str((col+1)%6 if (col+1)%6 != 0 else 6) +' '+ timetable[col][0] + '</td>')
            else:
                print('<td>' + str((col+1)%6 if (col+1)%6 != 0 else 6) +' '+ timetable[col][0] + '</td>')
        print('</tr>')
    print('</table>')



form = cgi.FieldStorage()
teacherID = form.getvalue('teacherID')
values = {'teacherID':teacherID}

db = sqlite3.connect('synergetic.db')
cursor = db.cursor()
cursor.execute('PRAGMA foreign_keys = ON')

cursor.execute('SELECT Period_Num, Class, Room FROM TeacherPeriods WHERE Teacher = :teacherID', values)
periods = cursor.fetchall()

startHTML('Synergetic Lite', 'main')

print('<h1>Teacher Timetable</h1>')

print('<hr>')

print('<div class="mainSection">')

print_Timetable(periods)
print('</div>')
print('<a href="teachersManage.py"><div class="backButton">Back</div></a>')
print('<hr>')

endHTML()
