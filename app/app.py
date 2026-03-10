import sqlite3

# connect to the database file
db = sqlite3.connect("database.db")
cur = db.cursor()

# addInstrument()
# adds an instrument with given fields to the database
def addInstrument():
    cur.execute("CREATE TABLE instrument(ID, Name_ID, Old_ID, Type, Grade, Make, Model, Picture, Serial_Number, Price, Stored_In, Dept)")

addInstrument()