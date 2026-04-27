import sqlite3

# addDepartment(Department_Name: str):
# adds a department with given fields to the database
def addDepartment(conn: Connection, Department_Name: str):
    # set cursor for db interaction
    cur = conn.cursor()

    # fetch latest ID to populate the new ID field with
    prevID = cur.execute("SELECT ID FROM department ORDER BY ID DESC LIMIT 1")
    prevID = cur.fetchone()[0]
    newID = str(prevID + 1 if prevID != None else 1)

    # str() everything else
    Department_Name = str(Department_Name)
    cur.execute("INSERT INTO department VALUES (" + newID + ",\'" + Department_Name + "\')")

    # commit changes to db file
    conn.commit()

    return newID