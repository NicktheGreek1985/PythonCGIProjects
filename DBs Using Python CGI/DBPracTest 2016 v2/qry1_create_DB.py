#!/usr/bin/python
print('Content-type: text/html\n')

import cgi
import cgitb; cgitb.enable()
import sqlite3

print '<p><a href="PracTest.html">Return to main test page</a></p>'
mydb = 'theworld.db'
conn = sqlite3.connect(mydb)

cursor = conn.cursor()

# Drop tables from DB if they exist
print('Drop tables if they exist<br />')
cursor.execute('''DROP TABLE IF EXISTS City''')
cursor.execute('''DROP TABLE IF EXISTS Continent''')
cursor.execute('''DROP TABLE IF EXISTS Country''')
cursor.execute('''DROP TABLE IF EXISTS EthnicGroup''')
cursor.execute('''DROP TABLE IF EXISTS Language''')
cursor.execute('''DROP TABLE IF EXISTS Population''')
cursor.execute('''DROP TABLE IF EXISTS Religion''')
cursor.execute('''DROP TABLE IF EXISTS encompasses''')

# Create tables
print('Create City table<br />')
cursor.execute('''CREATE TABLE City (
	CityID 		INTEGER PRIMARY KEY AUTOINCREMENT,
	Name		VARCHAR(35),
	Country		VARCHAR(4),
	Province	VARCHAR(35),
	Population	INT,
	Longitude	FLOAT,
	Latitude	FLOAT
)''')

print('Create Continent table<br />')
cursor.execute('''CREATE TABLE Continent (
	Name		VARCHAR(20),
	Area		FLOAT(10),
	PRIMARY KEY(Name)
)''')


print('Create Country table<br />')
cursor.execute('''CREATE TABLE Country (
	Name		VARCHAR(35) NOT NULL UNIQUE,
	Code		VARCHAR(4) PRIMARY KEY,
	Capital		VARCHAR(35),
	Province	VARCHAR(35),
	Area		FLOAT,
	Population	INT
)''')

print('Create EthnicGroup table<br />')
cursor.execute('''CREATE TABLE EthnicGroup (
	Country		VARCHAR(4),
	Name		VARCHAR(50),
	Percentage	FLOAT,
	PRIMARY KEY(Country,Name)
)''')

print('Create Language table<br />')
cursor.execute('''CREATE TABLE Language (
	LanguageID 	INTEGER PRIMARY KEY AUTOINCREMENT,
	Country		VARCHAR(4),
	Name		VARCHAR(50),
	Percentage	FLOAT
)''')

print('Create Population table<br />')
cursor.execute('''CREATE TABLE Population (
	Country				VARCHAR(4),
	Population_Growth	FLOAT,
	Infant_Mortality	FLOAT,
	PRIMARY KEY(Country)
)''')

print('Create encompasses table<br />')
cursor.execute('''CREATE TABLE encompasses (
	Country		VARCHAR(4) NOT NULL,
	Continent	VARCHAR(20) NOT NULL,
	Percentage	FLOAT,
	PRIMARY KEY(Country,Continent)
)''')


#******************************************************
# THIS IS THE SECTION YOU WILL HAVE TO CHANGE
#
# Add the SQL to create the Religion table here
print('Create Religion table<br />')
cursor.execute('''
			   ''')
#
#******************************************************


conn.commit()
cursor.close()
print 'new database created'
