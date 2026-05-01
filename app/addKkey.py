import sqlite3

# addKkey(Name_ID: str, Qty: int, Description: str):
# adds a kkey with given fields to the database
# the description field is for any additional information about the kkey, such as what it opens or where it is stored
def addKkey(conn, Name_ID, Qty=0, Description=""):
    # set cursor for db interaction
    cur = conn.cursor()

    # fetch latest ID safely
    cur.execute("SELECT ID FROM kkey ORDER BY ID DESC LIMIT 1")
    result = cur.fetchone()
    # empty table case
    newID = (result[0] + 1) if result and result[0] is not None else 1

    # parameterized querying
    sql = "INSERT INTO kkey (ID, Name_ID, Qty, Description) VALUES (?, ?, ?, ?)"
    params = (newID, str(Name_ID), Qty, str(Description))

    cur.execute(sql, params)
    
    # commit changes to db file
    conn.commit()

    return newID