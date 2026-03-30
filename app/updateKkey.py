import sys
import sqlite3

import updateIfNotNull

# connect to the database file
db = sqlite3.connect("database.db")
cur = db.cursor()

# updateKkey(ID: int, Name_ID: str, Qty: int, Description: str):
# updates a Kkey record with given fields in the database
def updateKkey(ID: int, Name_ID: str, Qty: int, Description: str):
    cur.execute("UPDATE broken SET " + updateIfNotNull.uINN("Name_ID", Name_ID) + ", " + updateIfNotNull.uINN("Qty", Qty) + ", " + updateIfNotNull.uINN("Description", Description) + " WHERE ID = " + str(ID))

# call function with passed arguments
updateKkey(int(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3]), str(sys.argv[4]))

# commit changes to db file
db.commit()

# close db connection
db.close()