#!/usr/bin/python
print('Content-type: text/html\n\n')

import cgi
import cgitb; cgitb.enable()
import sqlite3

mydb = 'videostore.db'
conn = sqlite3.connect(mydb)
cursor = conn.cursor()

print('Drop tables if they exist<br />')
cursor.execute('''DROP TABLE IF EXISTS Movie''')
cursor.execute('''DROP TABLE IF EXISTS Member''')

print('create Video table<br />')
cursor.execute('''CREATE TABLE Movie
                    (movie_id INTEGER PRIMARY KEY,
                    name VARCHAR(20) NOT NULL,
                    genre VARCHAR(10),
                    year INTEGER,
                    member_id INTEGER, FOREIGN KEY (member_id) REFERENCES Members(member_id), CHECK (year > 1950 AND year < 2020))''')

print('create Member table<br />')
cursor.execute('CREATE TABLE Member(member_id INTEGER PRIMARY KEY, first_name VARCHAR(20) NOT NULL, last_name VARCHAR(20) NOT NULL, phone VARCHAR(20) DEFAULT "999 999-999")')

conn.commit()
cursor.close()
