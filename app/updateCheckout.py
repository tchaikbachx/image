import sqlite3

# updates only the provided fields for a specific checkout record; if a
# parameter is None, that column in the db remains unchanged
def updateCheckout(conn, ID, Borrower_ID=None, Item_ID=None, Checkout_Date=None, Due_Date=None, Closed_Date=None):
    # mapping them
    updates = {
        "Borrower_ID": Borrower_ID,
        "Item_ID": Item_ID,
        "Checkout_Date": Checkout_Date,
        "Due_Date": Due_Date,
        "Closed_Date": Closed_Date
    }

    # filter out any keys where the value is None
    to_update = {k: v for k, v in updates.items() if v is not None}

    if not to_update:
        return False  # nothing to update

    # dynamically build this
    set_clause = ", ".join([f"{column} = ?" for column in to_update.keys()])
    params = list(to_update.values())
    params.append(ID)

    query = f"UPDATE checkout SET {set_clause} WHERE ID = ?"

    try:
        cur = conn.cursor()
        cur.execute(query, params)
        conn.commit()
        return cur.rowcount > 0
    except sqlite3.Error as e:
        print(f"SQL Error in updateCheckout: {e}")
        return False