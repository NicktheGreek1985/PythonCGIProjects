#!/usr/bin/python
print('Content-type: text/html\n')

'''

Synergetic Lite

manageClassTimetable.py

Creates HTML page to display the timetable for a class.
Allows user to attempt to allocate periods using links on the free ones.

By Nick Patrikeos on 22DEC17

'''

import cgi
import cgitb; cgitb.enable()
import sqlite3
from dbFunctions import *

def print_Timetable(t, classID):
    #### WE ALSO NEED classID

    # Prints out the periods in correct order
    # t is a single ordered array containing all periods a student has
    timetable = []
    for period in range(30):
        if period in [28, 29,18]:
            timetable.append(('RESERVED', 0))
        elif period in [ i[0] for i in t]:
            timetable.append(('<form action="removePeriodReservation.py" id="deleteForm"><input type="text" name="periodNum" value="' +
            str(period) + '" /><input type="text" name="classID" value="' + classID + '" /><input type="submit" style="color: white" value="Remove"/></form>', 1))
        else:
            timetable.append(('<form action="reservePeriod.py" id="deleteForm"><input type="text" name="periodNum" value="' +
            str(period) + '" /><input type="text" name="classID" value="' + classID + '" /><input type="submit" style="color: white" value="Reserve"/></form>', 2))

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
                print('<td style="background-color: rgb(45, 136, 205)">' + str((col+1)%6 if (col+1)%6 != 0 else 6) +' '+ 'RESERVED' + '</td>')
            elif timetable[col][1] == 1:
                print('<td style="background-color: #dd514c; color: white">' + str((col+1)%6 if (col+1)%6 != 0 else 6) +' '+ timetable[col][0] + '</td>')
            elif timetable[col][1] == 2:
                print('<td style="background-color: #5eb95e; color: white">' + str((col+1)%6 if (col+1)%6 != 0 else 6) +' '+ timetable[col][0] + '</td>')
            else:
                print('<td>' + str((col+1)%6 if (col+1)%6 != 0 else 6) +' '+ timetable[col][0] + '</td>')
        print('</tr>')
    print('</table>')



form = cgi.FieldStorage()
classID = form.getvalue('classID')
values = {'classID':classID}

db = sqlite3.connect('synergetic.db')
cursor = db.cursor()
cursor.execute('PRAGMA foreign_keys = ON')

cursor.execute('SELECT Teacher FROM Classes WHERE Class_ID = :classID', values)
records = cursor.fetchall()
teacherID = records[0][0]

cursor.execute('SELECT Period_Num, Room FROM TeacherPeriods WHERE Class = :classID', values)
periods = cursor.fetchall()

startHTML('Synergetic Lite', 'main')

print('<h1>Class Timetable Management</h1>')

print('<hr>')

fieldnames = ['ID', 'Teacher', 'Course', 'Actions']

print('<div class="mainSection">')

print_Timetable(periods, classID)
print('</div>')
print('<a href="classesManage.py"><div class="backButton">Back</div></a>')
print('<hr>')

endHTML()
