import sqlite3

import updateIfNotNull

# updateLocker(ID: int, Name_ID: str, Combo: str, Kkey: int, Checkoutable: bool):
# >> where args contains the list of data to be updated
# updates a locker record with given fields in the database
def updateLocker(conn, ID, **args):
    cur = conn.cursor()
    
    # filter out None values to build <set>
    updates = []
    params = []
    
    for key, value in args.items():
        if value is not None:
            updates.append(f"{key} = ?")
            params.append(value)
    
    if not updates:
        return False

    # dynamically build string
    sql = f"UPDATE locker SET {', '.join(updates)} WHERE ID = ?"
    params.append(ID)
    
    cur.execute(sql, params)
    conn.commit()
    return cur.rowcount > 0