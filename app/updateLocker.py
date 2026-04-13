import sqlite3

import updateIfNotNull

# connect to the database file
db = sqlite3.connect("database.db")
cur = db.cursor()

# updateLocker(ID: int, Name_ID: str, Combo: str, Kkey: int, Checkoutable: bool):
# updates a locker record with given fields in the database
def updateLocker(conn: Connection, ID: int, Name_ID: str, Combo: str, Kkey: int, Checkoutable: bool):
    # set cursor for db interaction
    cur = conn.cursor()

    cur.execute("UPDATE broken SET " + updateIfNotNull.uINN("Name_ID", Name_ID) + ", " + updateIfNotNull.uINN("Combo", Combo) + ", " + updateIfNotNull.uINN("Kkey", Kkey) + ", " + updateIfNotNull.uINN("Checkoutable", Checkoutable) + " WHERE ID = " + str(ID))

    # commit changes to db file
    conn.commit()