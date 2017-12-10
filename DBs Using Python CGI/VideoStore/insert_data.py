#!/usr/bin/python
print('Content-type: text/html\n\n')

import cgi
import cgitb; cgitb.enable()
import sqlite3

mydb = 'videostore.db'
conn = sqlite3.connect(mydb)
cursor = conn.cursor()

print('start inserting data into Movie table<br />')
cursor.execute('''INSERT INTO Movie (movie_id, name, genre, year) VALUES (34575, "The Shawshank Redemption", "Drama", 1994)''')
cursor.execute('''INSERT INTO Movie (movie_id, name, genre, year) VALUES (34697, "The Good, the Bad and the Ugly", "Western", 1966)''')
cursor.execute('''INSERT INTO Movie (movie_id, name, genre, year) VALUES (44573, "The Lord of the Rings: The Return of the King", "Fantasy", 2003)''')
cursor.execute('''INSERT INTO Movie (movie_id, name, genre, year) VALUES (45789, "The Usual Suspect", "Thriller", 1995)''')
cursor.execute('''INSERT INTO Movie (movie_id, name, genre, year) VALUES (34826, "The Silence of the Lambs", "Thriller", 1991)''')
cursor.execute('''INSERT INTO Movie (movie_id, name, genre, year) VALUES (67895, "Raiders of the Lost Ark", "Action", 1981)''')
cursor.execute('''INSERT INTO Movie (movie_id, name, genre, year) VALUES (68954, "Dark Knight Rises", "Action", 2012)''')
cursor.execute('''INSERT INTO Movie (movie_id, name, genre, year) VALUES (85484, "A Clockwork Orange", "Drama", 1971)''')
cursor.execute('''INSERT INTO Movie (movie_id, name, genre, year) VALUES (89577, "Kingsman: The Secret Service", "Comedy", 2014)''')
cursor.execute('''INSERT INTO Movie (movie_id, name, genre, year) VALUES (94354, "Zoolander", "Comedy", 2001)''')
print('finish inserting data into Movie table<br />')

print('start inserting data into the Member table<br />')
cursor.execute('''INSERT INTO Member (member_id, first_name, last_name, phone) VALUES (1001, "Isaiah", "Langley", "749 141 2253")''')
cursor.execute('''INSERT INTO Member (member_id, first_name, last_name, phone) VALUES (1008, "Connor", "Booth", "886 999 5163")''')
cursor.execute('''INSERT INTO Member (member_id, first_name, last_name, phone) VALUES (1026, "Joseph", "Higgins", "167 303 1679")''')
cursor.execute('''INSERT INTO Member (member_id, first_name, last_name, phone) VALUES (1060, "Steven", "Chang", "793 488 7281")''')
print('finish inserting data into the Member table<br />')
conn.commit()
cursor.close()
