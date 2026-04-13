import sqlite3

import updateIfNotNull

# connect to the database file
db = sqlite3.connect("database.db")
cur = db.cursor()

# updateBroken(ID: int, Date_Broken: str, Date_Fixed: str, Item_ID: int, Description: str):
# updates a broken item record with given fields in the database
def updateBroken(conn: Connection, ID: int, Date_Broken: str, Date_Fixed: str, Item_ID: int, Description: str):
    # set cursor for db interaction
    cur = conn.cursor()

    cur.execute("UPDATE broken SET " + updateIfNotNull.uINN("Date_Broken", Date_Broken) + ", " + updateIfNotNull.uINN("Date_Fixed", Date_Fixed) + ", " + updateIfNotNull.uINN("Item_ID", Item_ID) + ", " + updateIfNotNull.uINN("Description", Description) + " WHERE ID = " + str(ID))

    # commit changes to db file
    conn.commit()