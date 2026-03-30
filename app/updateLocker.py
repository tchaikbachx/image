import sys
import sqlite3

import updateIfNotNull

# connect to the database file
db = sqlite3.connect("database.db")
cur = db.cursor()

# updateLocker(ID: int, Name_ID: str, Combo: str, Kkey: int, Checkoutable: bool):
# updates a locker record with given fields in the database
def updateLocker(ID: int, Name_ID: str, Combo: str, Kkey: int, Checkoutable: bool):
    cur.execute("UPDATE broken SET " + updateIfNotNull.uINN("Name_ID", Name_ID) + ", " + updateIfNotNull.uINN("Combo", Combo) + ", " + updateIfNotNull.uINN("Kkey", Kkey) + ", " + updateIfNotNull.uINN("Checkoutable", Checkoutable) + " WHERE ID = " + str(ID))

# call function with passed arguments
updateLocker(int(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3]), str(sys.argv[4]), str(sys.argv[5]))

# commit changes to db file
db.commit()

# close db connection
db.close()