import sys

# setting path
sys.path.append('../image')

# importing
from manager import manager
import sqlite3
from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from flask_cors import CORS
import os

# connect to the database file

db_path = os.path.join(os.path.dirname(__file__), 'test.db')
man = manager(db_path)

db = sqlite3.connect(db_path)
cur = db.cursor()

# create dummy instrument objects
dummy = {'Name_ID': 'test', 'Old_ID': '0', 'Type': 'piano', 'Grade': 'excellent', 'Make': 'yamaha', 'Model': 'F250', 'Picture': 'imagine something', 'Serial_Number': '1337', 'Price': 'infinity', 'Stored_In': '2', 'Dept': '3'}
dummy2 = {'Name_ID': 'test2', 'Old_ID': '0', 'Type': 'piano', 'Grade': 'terrible', 'Make': 'yamaha', 'Model': 'F250', 'Picture': 'imagine something', 'Serial_Number': '1337', 'Price': 'infinity', 'Stored_In': '2', 'Dept': '3'}
securitydummy = {'Name_ID': 'test2', 'Old_ID': '0', 'Type': 'piano', 'Grade': 'terrible', 'Make': 'yamaha', 'Model': 'F250', 'Picture': 'imagine something', 'Serial_Number': '1337', 'Price': 'infinity', 'Stored_In': '2', 'Dept': '3', 'ID': '21 OR ID = ANY'}

# initTables()
# creates the tables in the db
def initTables():
    cur.execute("CREATE TABLE IF NOT EXISTS instrument(ID INT PRIMARY KEY, Name_ID, Old_ID, Type, Grade, Make, Model, Picture, Serial_Number, Price, Stored_In, Dept)")
    cur.execute("CREATE TABLE IF NOT EXISTS kkey(ID INT PRIMARY KEY, Name_ID, Qty, Description)")
    cur.execute("CREATE TABLE IF NOT EXISTS locker(ID INT PRIMARY KEY, Name_ID, Combo, Kkey, Checkoutable)")
    cur.execute("CREATE TABLE IF NOT EXISTS borrower(ID INT PRIMARY KEY, Email)")
    cur.execute("CREATE TABLE IF NOT EXISTS checkout(ID INT PRIMARY KEY, Borrower_ID, Item_ID, Checkout_Date, Due_Date, Closed_Date)")
    cur.execute("CREATE TABLE IF NOT EXISTS missing(ID INT PRIMARY KEY, Date_Missing, Date_Found, Item_ID, Description)")
    cur.execute("CREATE TABLE IF NOT EXISTS broken(ID INT PRIMARY KEY, Date_Broken, Date_Fixed, Item_ID, Description)")
    cur.execute("CREATE TABLE IF NOT EXISTS department(ID INT PRIMARY KEY, Department_Name)")
    cur.execute("CREATE TABLE IF NOT EXISTS trashcan(ID INT PRIMARY KEY, otherID, col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, col11, col12)")

# delTables()
# deletes every table in the db
def delTables():
    cur.execute("DROP TABLE IF EXISTS instrument")
    cur.execute("DROP TABLE IF EXISTS kkey")
    cur.execute("DROP TABLE IF EXISTS locker")
    cur.execute("DROP TABLE IF EXISTS borrower")
    cur.execute("DROP TABLE IF EXISTS checkout")
    cur.execute("DROP TABLE IF EXISTS missing")
    cur.execute("DROP TABLE IF EXISTS broken")
    cur.execute("DROP TABLE IF EXISTS department")
    cur.execute("DROP TABLE IF EXISTS trashcan")

# init tables
try:
    initTables()
    print("PASS test: initialized tables")
except Exception as e:
    print("FAIL test: failed to initialize tables (" + str(e) + ")")

# try to add a dummy instrument to the empty table
try:
    man.add('instrument', jsonify(dummy))
    print("PASS test: added dummy instrument to empty table")
except Exception as e:
    print("FAIL test: failed to add dummy instrument to empty table (" + str(e) + ")")

# try to add a second dummy instrument to the now non-empty table
try:
    man.add('instrument', jsonify(dummy))
    print("PASS test: added second dummy instrument to table")
except Exception as e:
    print("FAIL test: failed to add second dummy instrument to table (" + str(e) + ")")

# try to edit an entry
try:
    man.update('instrument', "1", jsonify(dummy2))
    print("PASS test: edited entry 1")
except Exception as e:
    print("FAIL test: failed to edit entry 1 (" + str(e) + ")")

# try to delete entry with ID = 0
try:
    man.delete('instrument', "0")
    print("PASS test: deleted entry 0")
except Exception as e:
    print("FAIL test: failed to delete entry 0 (" + str(e) + ")")

# try to add a dummy instrument back into table at ID = 0
try:
    man.add('instrument', jsonify(dummy))
    print("PASS test: added dummy instrument to table at ID = 0 after deletion")
except Exception as e:
    print("FAIL test: failed to add dummy instrument to table at ID = 0 after deletion (" + str(e) + ")")

# try to edit entry that doesn't exist
try:
    man.update('missing', "3", jsonify(dummy))
    print("FAIL test: did not throw exception trying to edit null entry")
except Exception as e:
    print("PASS test: threw exception trying to edit null entry (" + str(e) + ")")

# try to delete entry that doesn't exist
try:
    man.delete('missing', "3")
    print("FAIL test: did not throw exception trying to delete null entry")
except Exception as e:
    print("PASS test: threw exception trying to delete null entry (" + str(e) + ")")

# try to make an entry with bad data
try:
    man.add('instrument', jsonify(securitydummy))
    print("FAIL test: successfully added entry with bad data")
except Exception as e:
    print("PASS test: failed to add entry with bad data (" + str(e) + ")")

# delete test tables after testing finishes
delTables()
