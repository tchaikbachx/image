import sqlite3

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

# addInstrument()
# adds an instrument with given fields to the database
def addInstrument(ID, Name_ID, Old_ID, Type, Grade, Make, Model, Picture, Serial_Number, Price, Stored_In, Dept):
    cur.execute("INSERT INTO instrument VALUES (" + ID + "," + Name_ID + "," + Old_ID + "," + Type + "," + Grade + "," + Make + "," + Model + "," + Picture + "," + Serial_Number + "," + Price + "," + Stored_In + "," + Dept + ")")

# addKkey()
# adds a kkey with given fields to the database
# the description field is for any additional information about the kkey, such as what it opens or where it is stored
def addKkey(ID, Name_ID, Qty, Description):
    cur.execute("INSERT INTO kkey VALUES (" + ID + "," + Name_ID + "," + Qty + "," + Description + ")")

# addLocker()
# adds a locker with given fields to the database
# Checkoutable is a boolean field that indicates whether the locker can be checked out or not
def addLocker(ID, Name_ID, Combo, Kkey, Checkoutable):
    cur.execute("INSERT INTO locker VALUES (" + ID + "," + Name_ID + "," + Combo + "," + Kkey + "," + Checkoutable + ")")

# addBorrower()
# adds a borrower with given fields to the database
def addBorrower(ID, Email):
    cur.execute("INSERT INTO borrower VALUES (" + ID + "," + Email + ")")

# addCheckout()
# adds a checkout record with given fields to the database
def addCheckout(ID, Borrower_ID, Item_ID, Checkout_Date, Due_Date, Closed_Date):
    cur.execute("INSERT INTO checkout VALUES (" + ID + "," + Borrower_ID + "," + Item_ID + "," + Checkout_Date + "," + Due_Date + "," + Closed_Date + ")")

# addMissing()
# adds a missing item record with given fields to the database
def addMissing(ID, Date_Missing, Date_Found, Item_ID, Description):
    cur.execute("INSERT INTO missing VALUES (" + ID + "," + Date_Missing + "," + Date_Found + "," + Item_ID + "," + Description + ")")

# addBroken()
# adds a broken item record with given fields to the database
def addBroken(ID, Date_Broken, Date_Fixed, Item_ID, Description):
    cur.execute("INSERT INTO broken VALUES (" + ID + "," + Date_Broken + "," + Date_Fixed + "," + Item_ID + "," + Description + ")")

# addDepartment()
# adds a department with given fields to the database
def addDepartment(ID, Department_Name):
    cur.execute("INSERT INTO department VALUES (" + ID + "," + Department_Name + ")")




#----- FUNCTIONS ABOVE ----- CALLS BELOW -----#

# initialize tables
initTables()


#----- function calls to add entries to the database, for testing purposes:
#addInstrument("2", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12")
#addKkey("2", "'K25'", "3", "4")
#addLocker("1", "2", "3", "4", "5")
# addBorrower("1", "2")
# addCheckout("1", "2", "3", "4", "5", "6")
# addMissing("1", "2", "3", "4", "5")
# addBroken("1", "2", "3", "4", "5")
# addDepartment("1", "2")


# commit changes to db file
db.commit()

# close db connection
db.close()