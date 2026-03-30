import sys
import sqlite3

import updateIfNotNull

# connect to the database file
db = sqlite3.connect("database.db")
cur = db.cursor()

# updateMissing(ID: int, Date_Missing: str, Date_Found: str, Item_ID: int, Description: str):
# updates a missing item record with given fields in the database
def updateMissing(ID: int, Date_Missing: str, Date_Found: str, Item_ID: int, Description: str):
    cur.execute("UPDATE broken SET " + updateIfNotNull.uINN("Date_Missing", Date_Missing) + ", " + updateIfNotNull.uINN("Date_Found", Date_Found) + ", " + updateIfNotNull.uINN("Item_ID", Item_ID) + ", " + updateIfNotNull.uINN("Description", Description) + " WHERE ID = " + str(ID))

# call function with passed arguments
updateMissing(int(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3]), str(sys.argv[4]), str(sys.argv[5]))

# commit changes to db file
db.commit()

# close db connection
db.close()