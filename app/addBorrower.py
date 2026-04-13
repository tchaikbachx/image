import sqlite3

# addBorrower(Email: str):
# adds a borrower with given fields to the database
def addBorrower(conn: Connection, Email: str):
    # set cursor for db interaction
    cur = conn.cursor()

    # fetch latest ID to populate the new ID field with
    prevID = cur.execute("SELECT ID FROM borrower ORDER BY ID DESC LIMIT 1")
    prevID = cur.fetchone()[0]

    # str() everything else
    Email = str(Email)
    cur.execute("INSERT INTO borrower VALUES (" + str(prevID + 1 if prevID != None else 1) + ",\'" + Email + "\')")

    # commit changes to db file
    conn.commit()