import sqlite3

# update the checkout table accordingly
def updateCheckout(conn, ID, Borrower_ID, Item_ID, Checkout_Date, Due_Date, Closed_Date):
    cur = conn.cursor()
    
    query = """
        UPDATE checkout 
        SET Borrower_ID = ?, 
            Item_ID = ?, 
            Checkout_Date = ?, 
            Due_Date = ?, 
            Closed_Date = ? 
        WHERE ID = ?
    """
    
    # simplified it
    params = (Borrower_ID, Item_ID, Checkout_Date, Due_Date, Closed_Date, ID)
    
    try:
        cur.execute(query, params)
        conn.commit()
        return cur.rowcount > 0
    except sqlite3.Error as e:
        print(f"SQL Error in updateCheckout: {e}")
        return False