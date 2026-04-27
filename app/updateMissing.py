import sqlite3

import updateIfNotNull

# updateMissing(ID: int, Date_Missing: str, Date_Found: str, Item_ID: int, Description: str):
# updates a missing item record with given fields in the database
def updateMissing(conn: Connection, ID: int, Date_Missing: str, Date_Found: str, Item_ID: int, Description: str):
    # set cursor for db interaction
    cur = conn.cursor()

    cur.execute("UPDATE broken SET " + updateIfNotNull.uINN("Date_Missing", Date_Missing) + ", " + updateIfNotNull.uINN("Date_Found", Date_Found) + ", " + updateIfNotNull.uINN("Item_ID", Item_ID) + ", " + updateIfNotNull.uINN("Description", Description) + " WHERE ID = " + str(ID))

    # commit changes to db file
    conn.commit()

    # empty table check
    return cur.rowcount > 0