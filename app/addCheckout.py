import sqlite3
from datetime import date

def addCheckout(conn, Item_ID, Borrower_ID, Due_Date):
    cur = conn.cursor()

    # 1. Fetch latest ID - Handle the "Empty Table" case
    cur.execute("SELECT ID FROM checkout ORDER BY ID DESC LIMIT 1")
    result = cur.fetchone()
    
    if result is None:
        newID = 1
    else:
        newID = result[0] + 1

    # 2. Insert the new checkout record
    # the columns are (ID, Item_ID, Borrower_ID, Return_Date)

    query = "INSERT INTO checkout (ID,  Borrower_ID, Item_ID, Checkout_Date, Due_Date) VALUES (?, ?, ?, ?, ?)"
    cur.execute(query, (newID, Borrower_ID, Item_ID, date.today(), Due_Date))

    conn.commit()
    return newID