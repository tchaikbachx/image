import sqlite3

# connect to the database file
db = sqlite3.connect("database.db")
cur = db.cursor()

# addDepartment(Department_Name: str):
# adds a department with given fields to the database
def addDepartment(conn: Connection, Department_Name: str):
    # set cursor for db interaction
    cur = conn.cursor()

    # fetch latest ID to populate the new ID field with
    prevID = cur.execute("SELECT ID FROM department ORDER BY ID DESC LIMIT 1")
    prevID = cur.fetchone()[0]

    # str() everything else
    Department_Name = str(Department_Name)
    cur.execute("INSERT INTO department VALUES (" + str(prevID + 1 if prevID != None else 1) + ",\'" + Department_Name + "\')")

    # commit changes to db file
    conn.commit()