import sys
import sqlite3


# connect to the database file
db = sqlite3.connect("database.db")
cur = db.cursor()

# addDepartment()
# adds a department with given fields to the database
def addDepartment(Department_Name: str):
    # fetch latest ID to populate the new ID field with
    prevID = cur.execute("SELECT ID FROM department ORDER BY ID DESC")
    prevID = cur.fetchone()[0]

    # str() everything else
    Department_Name = str(Department_Name)
    cur.execute("INSERT INTO department VALUES (" + str(prevID + 1 if prevID != None else 1) + ",\'" + Department_Name + "\')")

# call function with passed arguments
addDepartment(str(sys.argv[1]))

# commit changes to db file
db.commit()

# close db connection
db.close()