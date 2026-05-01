import sqlite3

# add a checkout to the table and update the history accordingly.
def addCheckout(conn, Item_ID, Borrower_ID, Due_Date):
    cur = conn.cursor()

    # get ID
    cur.execute("SELECT ID FROM checkout ORDER BY ID DESC LIMIT 1")
    result = cur.fetchone()
    
    # null/empty protection
    if result is None:
        newID = 1
    else:
        newID = result[0] + 1

    # insert into checkout table
    query = "INSERT INTO checkout (ID, Item_ID, Borrower_ID, Due_Date) VALUES (?, ?, ?, ?)"
    cur.execute(query, (newID, Item_ID, Borrower_ID, Due_Date))

    conn.commit()
    return newID