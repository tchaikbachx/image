import sys
import sqlite3


# connect to the database file
db = sqlite3.connect("database.db")
cur = db.cursor()

# addBorrower(Email: str):
# adds a borrower with given fields to the database
def addBorrower(Email: str):
    # fetch latest ID to populate the new ID field with
    prevID = cur.execute("SELECT ID FROM borrower ORDER BY ID DESC")
    prevID = cur.fetchone()[0]

    # str() everything else
    Email = str(Email)
    cur.execute("INSERT INTO borrower VALUES (" + str(prevID + 1 if prevID != None else 1) + ",\'" + Email + "\')")

# call function with passed arguments
addBorrower(str(sys.argv[1]))

# commit changes to db file
db.commit()

# close db connection
db.close()