import sys
import sqlite3

import updateIfNotNull

# connect to the database file
db = sqlite3.connect("database.db")
cur = db.cursor()

# updateDepartment(ID: int, Department_Name: str):
# updates a department record with given fields in the database
def updateDepartment(ID: int, Department_Name: str):
    cur.execute("UPDATE department SET " + updateIfNotNull.uINN("Department_Name", Department_Name) + " WHERE ID = " + str(ID))

# call function with passed arguments
updateDepartment(int(sys.argv[1]), str(sys.argv[2]))

# commit changes to db file
db.commit()

# close db connection
db.close()