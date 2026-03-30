import sys
import sqlite3

# connect to the database file
db = sqlite3.connect("database.db")
cur = db.cursor()

# deleteEntry(table: str, ID: int):
# deletes a row of table `table` with ID `ID`
def deleteEntry(table: str, ID: int):
    cur.execute("DELETE " + table + " WHERE ID = " + str(ID))

# call function with passed arguments
deleteEntry(str(sys.argv[1]), int(sys.argv[2]))

# commit changes to db file
db.commit()

# close db connection
db.close()