import sys
import sqlite3


# connect to the database file
db = sqlite3.connect("database.db")
cur = db.cursor()

# addKkey(Name_ID: str, Qty: int, Description: str):
# adds a kkey with given fields to the database
# the description field is for any additional information about the kkey, such as what it opens or where it is stored
def addKkey(Name_ID: str, Qty: int, Description: str):
    # fetch latest ID to populate the new ID field with
    prevID = cur.execute("SELECT ID FROM kkey ORDER BY ID DESC")
    prevID = cur.fetchone()[0]

    # str() everything else
    Name_ID = str(Name_ID)
    Qty = str(Qty)
    Description = str(Description)
    cur.execute("INSERT INTO kkey VALUES (" + str(prevID + 1 if prevID != None else 1) + ",\'" + Name_ID + "\'," + Qty + ",\'" + Description + "\')")

# call function with passed arguments
addKkey(str(sys.argv[1]), int(sys.argv[2]), str(sys.argv[3]))

# commit changes to db file
db.commit()

# close db connection
db.close()