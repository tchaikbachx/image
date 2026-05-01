import sqlite3

# addLocker(Name_ID: str, Combo: str, Kkey: int, Checkoutable: bool):
# adds a locker with given fields to the database
# Checkoutable is a boolean field that indicates whether the locker can be checked out or not
def addLocker(conn, Name_ID, Combo=None, Kkey=None, Checkoutable=1):
    cur = conn.cursor()

    # get next ID
    cur.execute("SELECT ID FROM locker ORDER BY ID DESC LIMIT 1")
    result = cur.fetchone()
    newID = (result[0] + 1) if result else 1

    # modified this to avoid syntax/quote errors
    sql = "INSERT INTO locker (ID, Name_ID, Combo, Kkey, Checkoutable) VALUES (?, ?, ?, ?, ?)"
    # guard
    params = (
        newID, 
        Name_ID, 
        Combo if Combo is not None else "N/A", 
        Kkey if Kkey is not None else 0, # assuming 0/None for key
        Checkoutable
    )

    cur.execute(sql, params)
    conn.commit()
    
    return newID