import sqlite3

db = sqlite3.connect('marks.db')
db.execute('DROP TABLE IF EXISTS DTH')
db.execute('CREATE TABLE DTH (Assessment TEXT, Raw_Mark TEXT, Percentage INT, Weighting FLOAT)')
