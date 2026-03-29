import sqlite3
import datetime

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

# toydb 
def toydb():
    # this function is for testing purposes, it adds some entries to the database 
    # add lockers
    addLocker("3", "'A1'", "'1234'", "0", "'yes'")
    addLocker("4", "'A2'", "'2345'", "0", "'yes'")
    addLocker("5", "'A3'", "'3456'", "0", "'no'")
    addLocker("6", "'A4'", "'0'", "8", "'yes'")
    addLocker("7", "'A5'", "'0'", "9", "'no'")

    # add kkeys
    addKkey("8", "'K17'", "1", "'Opens Locker A4'")
    addKkey("9", "'M22'", "3", "'Opens Locker A5'")

    # add instruments
    addInstrument("10", "'Violin1'", "123", "'Violin'", "'A'", "'Sibelius'", "'model'", "'image'", "'12345'", '1000', "'3'", "'16'")
    addInstrument("11", "'Violin2'", "234", "'Violin'", "'B'", "'Stradivarius'", "'model'", "'image'", "'12345'", '1000', "'4'", "'16'")
    addInstrument("12", "'Violin3'", "345", "'Violin'", "'C'", "'Yamaha'", "'model'", "'image'", "'12345'", '1000', "'5'", "'16'")
    addInstrument("13", "'Guitar1'", "456", "'Guitar'", "'A'", "'Yamaha'", "'model'", "'image'", "'12345'", '1000', "'6'", "'16'")
    addInstrument("14", "'Guitar2'", "567", "'Guitar'", "'B'", "'Yamaha'", "'model'", "'image'", "'12345'", '1000', "'6'", "'16'")
    addInstrument("15", "'Mandolin1'", "678", "'String'", "'A'", "'Ancienct'", "'model'", "'image'", "'12345'", '1000', "'Early Music Room'","'17'")

    # add department
    addDepartment("16", "'Music Checkout'")
    addDepartment("17", "'Early Music Room'")

    # add borrowers
    addBorrower("18", "'marshall@grinnell.edu'")
    addBorrower("19", "'johndoe@example.com'")
    addBorrower("20", "'pmosera@grinnell.edu'")

    # add checkouts
    addCheckout("21", "18", "10", "'3/26/26'", "'4/26/26'", "'0'")
    addCheckout("22", "20", "11", "'3/27/26'", "'4/27/26'", "'5/23/26'")
    addCheckout("23", "20", "13", "'3/4/34'", "'3/5/36'", "'0'")
    addCheckout("24", "20", "14", "'4/5/45'", "'2/3/46'", "'0'")

    # add missing items
    addMissing("25", "'3/26/26'", "'0'", "15", "'missing mandolin'")
    addMissing("26", "'3/27/26'", "'4/1/26'", "14", "'missing guitar'")

    # add broken items
    addBroken("27", "'3/26/26'", "'0'", "15", "'broken mandolin'")
    addBroken("28", "'3/27/26'", "'4/1/26'", "14", "'broken guitar'")

    #----- end of long function


#----- FUNCTIONS ABOVE ----- CALLS BELOW -----#

# initialize tables
initTables()




#----- function calls to add entries to the database, for testing purposes:
#toydb()
# addDepartment(29, 'TDPS')
# addBroken(30, '3/26/26', '0', 12, 'broken violin')
# addBroken(31, '3/27/26', '4/1/26', 13, 'broken guitar')
# addMissing(32, '3/26/26', '0', 13, 'missing guitar')
# addCheckout(33, 19, 12, '3/28/26', '4/28/26', '0')
# addBorrower(34, 'DoctorWho@whatishappening.org')
# addLocker(35, 'A6', '0', 9, True)
# addKkey(36, 'K18', 1, 'Opens auditorium storage closet')
# addInstrument(37, 'Flute1', '789', 'Flute', 'A', 'Yamaha', 'model', 'image', '12345', 304.33, 35, 16)

# commit changes to db file
db.commit()

# close db connection
db.close()