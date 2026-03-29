import sys
import sqlite3


# connect to the database file
db = sqlite3.connect("database.db")
cur = db.cursor()

# addInstrument()
# adds an instrument with given fields to the database
def addInstrument(Name_ID: str, Old_ID: str, Type: str, Grade: str, Make: str, Model: str, Picture: str, Serial_Number: str, Price: float, Stored_In: int, Dept: int):
    # fetch latest ID to populate the new ID field with
    prevID = cur.execute("SELECT ID FROM instrument ORDER BY ID DESC")
    prevID = cur.fetchone()[0]

    # str() everything else
    Name_ID = str(Name_ID)
    Old_ID = str(Old_ID)
    Type = str(Type)
    Grade = str(Grade)
    Make = str(Make)
    Model = str(Model)
    Picture = str(Picture)
    Serial_Number = str(Serial_Number)
    Price = str(Price)
    Stored_In = str(Stored_In)
    Dept = str(Dept)
    cur.execute("INSERT INTO instrument VALUES (" + str(prevID + 1 if prevID != None else 1) + ",\'" + Name_ID + "\',\'" + Old_ID + "\',\'" + Type + "\',\'" + Grade + "\',\'" + Make + "\',\'" + Model + "\',\'" + Picture + "\',\'" + Serial_Number + "\'," + Price + "," + Stored_In + "," + Dept + ")")

# call function with passed arguments
addInstrument(str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3]), str(sys.argv[4]), str(sys.argv[5]), str(sys.argv[6]), str(sys.argv[7]), str(sys.argv[8]), float(sys.argv[9]), int(sys.argv[10]), int(sys.argv[11]))

# commit changes to db file
db.commit()

# close db connection
db.close()