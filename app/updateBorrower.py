import sys
import sqlite3

import updateIfNotNull

# connect to the database file
db = sqlite3.connect("database.db")
cur = db.cursor()

# updateBorrower(ID: int, Email: str):
# updates a borrower record with given fields in the database
def updateBorrower(ID: int, Email: str):
    cur.execute("UPDATE borrower SET " + updateIfNotNull.uINN("Email", Email) + " WHERE ID = " + str(ID))

# call function with passed arguments
updateBorrower(int(sys.argv[1]), str(sys.argv[2]))

# commit changes to db file
db.commit()

# close db connection
db.close()