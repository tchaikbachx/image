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

# cur.execute("DELETE FROM locker WHERE ID IS NULL")
# print(cur.execute("SELECT * FROM locker WHERE ID IS NULL").fetchall())


#----- FUNCTIONS ABOVE ----- CALLS BELOW -----#

# initialize tables
initTables()

# commit changes to db file
db.commit()

# close db connection
db.close()