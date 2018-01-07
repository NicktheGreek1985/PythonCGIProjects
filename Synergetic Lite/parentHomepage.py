#!/usr/bin/python
print('Content-type: text/html\n')

'''

Synergetic Lite

PARENT SIDE

parentHomepage.py

Creates HTML page to display:
- Recent unverified absences, with action to verify
- Recent verified absences, with actions to:
    - edit
    - remove
- Links to view all verified and unverified absences
- Classes for their student
- Student's timetable

By Nick Patrikeos on 06JAN18

'''

import cgi
import cgitb; cgitb.enable()
import sqlite3
import datetime
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


db = sqlite3.connect('synergetic.db')
cursor = db.cursor()
cursor.execute('PRAGMA foreign_keys = ON')

form = cgi.FieldStorage()
parentID = form.getvalue('parentID')
values = {'parentID':parentID}

cursor.execute('SELECT Student FROM Parents WHERE Parent_ID = :parentID', values)
studentID = cursor.fetchall()[0][0]
values['studentID'] = studentID

now = datetime.datetime.now()
twoWeeksAgo = now - datetime.timedelta(14)
formattedDate = twoWeeksAgo.strftime('%Y-%m-%d')

cursor.execute('SELECT Period, Date, Absentee_U_ID FROM AbsenteesUnverified WHERE Student = :studentID AND NOT Is_Verified AND Date >= ' + formattedDate, values)
fieldnames1 = ['Period', 'Date','Actions']
absences = cursor.fetchall()

for a in range(len(absences)):
    absences[a] = (int(absences[a][0]) + 1, absences[a][1], '<form id="deleteForm" action="verifyAbsence.py"><input type="text" name="absenceID" value="' + str(absences[a][2]) +'"/>' +
                    '<input type="submit" value="Verify" /></form>',)

cursor.execute('SELECT Start_Time, End_Time, Verification FROM AbsenteesVerified WHERE Student = :studentID AND Start_Time >= ' + formattedDate, values)
fieldnames3 = ['Start Time', 'End Time', 'Verification','Actions']
verifiedAbsences = cursor.fetchall()

for a in range(len(verifiedAbsences)):
    verifiedAbsences[a] += ('<a href="#">Edit</a> <a href="#">Remove</a>',)

cursor.execute('SELECT Period_Num, Class, Room FROM StudentPeriods WHERE Student = :studentID', values)
periods = cursor.fetchall()

fieldnames2 = ['Class', 'Teacher', 'Course']
cursor.execute('SELECT Class FROM Enrolments WHERE Student = :studentID', values)
classes = cursor.fetchall()
for cl in range(len(classes)):
    cursor.execute('SELECT Teacher, Course FROM Classes WHERE Class_ID = :classID', {'classID':classes[cl][0]})
    r = cursor.fetchall()
    classes[cl] += (r[0][0], r[0][1])

startHTML('Synergetic Lite', 'main')

print('<h1>Parent Homepage</h1>')

print('<hr>')

print('<div class="mainSection">')
print('<h3>Recent Absences - Unverified</h3>')
print_Records(absences, fields=fieldnames1)
print('<form id="deleteForm" action="viewUnverifiedAbsences.py"><input type="text" name="parentID" value="' + parentID +'" /><div class="backButton"><input type="submit" value="All Unverified Absences" /></div></form>')
print('<hr>')

print('<h3>Recent Absences - Verified</h3>')
print_Records(verifiedAbsences, fields=fieldnames3)
print('<div class="backButton">All Verified Absences</div>')
print('<form id="deleteForm" action="addVerifiedAbsence.py"><input type="text" name="studentID" value="' + str(studentID) +'" /><div class="backButton"><input type="submit" value="Verify New Absence" /></div></form>')
print('<hr>')

print('<h3>Classes</h3>')
print_Records(classes, fieldnames2)
print('<div class="backButton">View Live Marks</div>')
print('<hr>')
print('<h3>Student Timetable</h3>')
print_Timetable(periods)
print('<a href="index.html"><div class="backButton">Logout</div></a>')
print('</div>')
print('<hr>')

endHTML()
