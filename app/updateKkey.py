import sqlite3

# updateKkey(ID: int, Name_ID: str, Qty: int, Description: str):
# updates a Kkey record with given fields in the database
def updateKkey(conn, ID, **args):
    # set cursor for db
    cur = conn.cursor()

    updates = []
    params = []
    
    for key, value in args.items():
        if value is not None:
            updates.append(f"{key} = ?")
            params.append(value)
    
    # if no data sent to update, just return
    if not updates:
        return False

    # build string
    sql = f"UPDATE kkey SET {', '.join(updates)} WHERE ID = ?"
    params.append(ID)

    cur.execute(sql, params)
    
    # commit changes to db file
    conn.commit()

    # empty table check
    return cur.rowcount > 0