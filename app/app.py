import sqlite3

# connect to the database file
db = sqlite3.connect("database.db")
cur = db.cursor()

# initTables()
# creates the tables in the db
def initTables():
    cur.execute("CREATE TABLE IF NOT EXISTS instrument(ID INT PRIMARY KEY, Name_ID, Old_ID, Type, Grade, Make, Model, Picture, Serial_Number, Price, Stored_In, Dept)")

# addInstrument()
# adds an instrument with given fields to the database
def addInstrument(ID, Name_ID, Old_ID, Type, Grade, Make, Model, Picture, Serial_Number, Price, Stored_In, Dept):

    cur.execute("INSERT INTO instrument VALUES (" + ID + "," + Name_ID + "," + Old_ID + "," + Type + "," + Grade + "," + Make + "," + Model + "," + Picture + "," + Serial_Number + "," + Price + "," + Stored_In + "," + Dept + ")")

# initialize tables
initTables()

addInstrument("1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12")

# commit changes to db file
db.commit()

# close db connection
db.close()