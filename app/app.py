import sqlite3
import datetime

# import exportAsCSV
# import addBorrower
# import addBroken
# import addCheckout
# import addDepartment
# import addInstrument
# import addKkey
# import addLocker
# import addMissing
import emptyTrash
import deleteEntry

from flask import Flask

app = Flask(__name__)
@app.route("/")
def home():
    return "Hello"
    
# connect to the database file
db = sqlite3.connect("database.db")
cur = db.cursor()

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

# cur.execute("DELETE FROM locker WHERE ID IS NULL")
# print(cur.execute("SELECT * FROM locker WHERE ID IS NULL").fetchall())


#----- FUNCTIONS ABOVE ----- CALLS BELOW -----#

# initialize tables
initTables()

# How to add stuff to trashcan: (these will be deleted from the database but kept on a new table called trashcan until emptyTrash(db) is called)
# emptyTrash.emptyTrash(db)
# deleteEntry.deleteEntry(db, "instrument", 41)
# deleteEntry.deleteEntry(db, "kkey", 41)
# deleteEntry.deleteEntry(db, "locker", 41)
# deleteEntry.deleteEntry(db, "department", 1)


# commit changes to db file
db.commit()

# close db connection
db.close()
