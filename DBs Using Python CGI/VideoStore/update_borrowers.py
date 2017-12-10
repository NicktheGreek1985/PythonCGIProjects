#!/usr/bin/python
print('Content-type: text/html\n\n')

import cgi
import cgitb; cgitb.enable()
import sqlite3

mydb = 'videostore.db'
conn = sqlite3.connect(mydb)
cursor = conn.cursor()

print('Updating Movie table with borrowers<br />')
cursor.execute('''UPDATE Movie SET member_id = 1026 WHERE movie_id = 34575 OR movie_id = 45789''')
cursor.execute('UPDATE Movie SET member_id = 1008 WHERE movie_id = 94354 OR movie_id = 85484 OR movie_id = 34826 OR movie_id = 34697')
cursor.execute('UPDATE Movie SET member_id = 1060 WHERE movie_id = 67895')
print('Finished updating Movie table<br />')
conn.commit()
cursor.close()
