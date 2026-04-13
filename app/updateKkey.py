import sqlite3

import updateIfNotNull

# updateKkey(ID: int, Name_ID: str, Qty: int, Description: str):
# updates a Kkey record with given fields in the database
def updateKkey(conn: Connection, ID: int, Name_ID: str, Qty: int, Description: str):
    # set cursor for db interaction
    cur = conn.cursor()

    cur.execute("UPDATE broken SET " + updateIfNotNull.uINN("Name_ID", Name_ID) + ", " + updateIfNotNull.uINN("Qty", Qty) + ", " + updateIfNotNull.uINN("Description", Description) + " WHERE ID = " + str(ID))

    # commit changes to db file
    conn.commit()

    # empty table check
    return cur.rowcount > 0