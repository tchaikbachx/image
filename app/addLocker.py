import sqlite3

# connect to the database file
db = sqlite3.connect("database.db")
cur = db.cursor()

# addLocker(Name_ID: str, Combo: str, Kkey: int, Checkoutable: bool):
# adds a locker with given fields to the database
# Checkoutable is a boolean field that indicates whether the locker can be checked out or not
def addLocker(conn: Connection, Name_ID: str, Combo: str, Kkey: int, Checkoutable: bool):
    # set cursor for db interaction
    cur = conn.cursor()

    # fetch latest ID to populate the new ID field with
    prevID = cur.execute("SELECT ID FROM locker ORDER BY ID DESC LIMIT 1")
    prevID = cur.fetchone()[0]

    # str() everything else
    Kkey = str(Kkey)
    Checkoutable = str(Checkoutable)
    cur.execute("INSERT INTO locker VALUES (" + str(prevID + 1 if prevID != None else 1) + ",\'" + Name_ID + "\',\'" + Combo if Combo != None else "N/A" + "\'," + Kkey if Kkey != None else "N/A" + ",\'" + Checkoutable + "\')")

    # commit changes to db file
    conn.commit()