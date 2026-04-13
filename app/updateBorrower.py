import sqlite3

import updateIfNotNull

# updateBorrower(ID: int, Email: str):
# updates a borrower record with given fields in the database
def updateBorrower(conn: Connection, ID: int, Email: str):
    # set cursor for db interaction
    cur = conn.cursor()

    cur.execute("UPDATE borrower SET " + updateIfNotNull.uINN("Email", Email) + " WHERE ID = " + str(ID))

    # commit changes to db file
    conn.commit()

    # empty table check
    return cur.rowcount > 0