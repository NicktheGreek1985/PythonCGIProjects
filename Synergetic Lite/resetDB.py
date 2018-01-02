'''

Synergetic Lite

resetDB.py
Restores the database tables and inserts some sample data.

By Nick Patrikeos on 12DEC17

'''

import sqlite3

def resetDBTables(cursor):
    # Drops existing tables in the DB and creates new ones

    print('Dropping existing tables.')

    tables = ['Classes','Enrolments','Students','Parents',
              'Rooms','Courses','StudentPeriods','TeacherPeriods',
              'AbsenteesVerified','AbsenteesUnverified',
              'Assessments','Marks','Teachers']

    for table in tables:
        print('Dropping:', table)
        cursor.execute('DROP TABLE IF EXISTS '+ table)

    print('====================')
    print('Creating new tables.')

    cursor.execute('PRAGMA foreign_keys = ON')

    cursor.execute('''CREATE TABLE Teachers
                   (Teacher_ID VARCHAR(5),
                   Password TEXT,
                   Is_Admin BOOLEAN,

                   PRIMARY KEY (Teacher_ID))''')

    cursor.execute('''CREATE TABLE Classes
                   (Class_ID VARCHAR(10),
                   Teacher VARCHAR(5),
                   Course VARCHAR(8),

                   PRIMARY KEY(Class_ID),
                   FOREIGN KEY (Teacher) REFERENCES Teachers(Teacher_ID) ON UPDATE CASCADE,
                   FOREIGN KEY (Course) REFERENCES Courses(Course_ID) ON UPDATE CASCADE)''')

    cursor.execute('''CREATE TABLE Enrolments
                   (Enrolment_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                   Student INTEGER,
                   Class VARCHAR(10),

                   FOREIGN KEY (Student) REFERENCES Students(Student_ID) ON UPDATE CASCADE,
                   FOREIGN KEY (Class) REFERENCES Classes(Class_ID) ON UPDATE CASCADE)''')

    cursor.execute('''CREATE TABLE Students
                   (Student_ID INTEGER,
                   Password TEXT,

                   PRIMARY KEY (Student_ID))''')


    cursor.execute('''CREATE TABLE Parents
                   (Parent_ID INTEGER,
                   Password TEXT,
                   Student INTEGER,

                   PRIMARY KEY(Parent_ID)
                   FOREIGN KEY(Student) REFERENCES Students(Student_ID) ON UPDATE CASCADE)''')

    cursor.execute('''CREATE TABLE Rooms
                   (Room_ID VARCHAR(6),

                   PRIMARY KEY(Room_ID))''')

    cursor.execute('''CREATE TABLE Courses
                   (Course_ID VARCHAR(8),

                   PRIMARY KEY(Course_ID))''')

    cursor.execute('''CREATE TABLE StudentPeriods
                   (S_Period_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                   Period_Num INTEGER,
                   Class VARCHAR(10),
                   Room VARCHAR(6),
                   Student INTEGER,

                   FOREIGN KEY(Class) REFERENCES Classes(Class_ID) ON UPDATE CASCADE,
                   FOREIGN KEY(Room) REFERENCES Rooms(Room_ID) ON UPDATE CASCADE,
                   FOREIGN KEY(Student) REFERENCES Students(Student_ID) ON UPDATE CASCADE)''')

    cursor.execute('''CREATE TABLE TeacherPeriods
                   (T_Period_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                   Period_Num INTEGER,
                   Class VARCHAR(10),
                   Room VARCHAR(6),
                   Teacher VARCHAR(5),

                   FOREIGN KEY(Class) REFERENCES Classes(Class_ID) ON UPDATE CASCADE,
                   FOREIGN KEY(Room) REFERENCES Rooms(Room_ID) ON UPDATE CASCADE,
                   FOREIGN KEY(Teacher) REFERENCES Teachers(Teacher_ID) ON UPDATE CASCADE)''')

    cursor.execute('''CREATE TABLE AbsenteesVerified
                   (Absentee_V_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                   Verification TEXT,
                   Start_Time SMALLDATETIME,
                   End_Time SMALLDATETIME,
                   Student INTEGER,

                   FOREIGN KEY(Student) REFERENCES Students (Student_ID) ON UPDATE CASCADE)''')

    cursor.execute('''CREATE TABLE AbsenteesUnverified
                   (Absentee_U_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                   Student INTEGER,
                   Period INTEGER,
                   Date DATE,

                   FOREIGN KEY (Student) REFERENCES Students(Student_ID) ON UPDATE CASCADE,
                   FOREIGN KEY (Period) REFERENCES StudentPeriods(S_Period_ID) ON UPDATE CASCADE)''')

    cursor.execute('''CREATE TABLE Assessments
                   (Assessment_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                   Out_Of INTEGER,
                   Weighting FLOAT,
                   Course VARCHAR(8),

                   FOREIGN KEY(Course) REFERENCES Courses(Course_ID) ON UPDATE CASCADE)''')

    cursor.execute('''CREATE TABLE Marks
                    (Mark_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    Student INTEGER,
                    Raw_Mark INTEGER,
                    Assessment INTEGER,

                    FOREIGN KEY(Student) REFERENCES Students(Student_ID) ON UPDATE CASCADE,
                    FOREIGN KEY(Assessment) REFERENCES Assessments(Assessment_ID) ON UPDATE CASCADE)''')

    print('New tables created.')

def insertSampleData(cursor):
    # Inserts some fake test data into the students, teachers and parents tables

    cursor.execute('''INSERT INTO Students (Student_ID, Password) VALUES (1019912, "abc123")''')
    cursor.execute('''INSERT INTO Teachers (Teacher_ID, Password, Is_Admin) VALUES ("NIP", "abc123", 1)''')
    cursor.execute('''INSERT INTO Parents (Parent_ID, Password, Student) VALUES (1687, "abc123", 1019912)''')


# Main program: resetting via verification from the user

db = sqlite3.connect('synergetic.db')
cursor = db.cursor()

verif = input('Are you sure you want to reset the db? (y/n) ')

if verif == 'y':
    resetDBTables(cursor)
    insertSampleData(cursor)
    db.commit()
    db.close()

    print('DB has been reset.')
else:
    print('Reset aborted.')
