import sqlite3

# import updateIfNotNull

# example call to ONLY change closed date: 
#   updateCheckout.updateCheckout(db, 6, None, None, None, None, "4/27/27")

# updateCheckout(ID: int, Borrower_ID: int, Item_ID: int, Checkout_Date: str, Due_Date: str, Closed_Date: str):
# updates a checkout item record with given fields in the database
def updateCheckout(conn: Connection, ID: int, Borrower_ID: int, Item_ID: int, Checkout_Date: str, Due_Date: str, Closed_Date: str):
    # set cursor for db interaction
    cur = conn.cursor()

    sID = str(ID)
    
    if Item_ID == None:
        cur.execute("SELECT Item_ID FROM checkout WHERE ID = " + sID)
        Item_ID = cur.fetchone()[0]
    
    if Borrower_ID == None:
        Borrower_ID = cur.execute("SELECT Borrower_ID FROM checkout WHERE ID = " + sID).fetchone()[0]
    
    if Checkout_Date == None:
        Checkout_Date = cur.execute("SELECT Checkout_Date FROM checkout WHERE ID = " + sID).fetchone()[0]
    
    if Due_Date == None:
        Due_Date = cur.execute("SELECT Due_Date FROM checkout WHERE ID = " + sID).fetchone()[0]

    if Closed_Date == None:
        Closed_Date = cur.execute("SELECT Closed_Date FROM checkout WHERE ID = " + sID).fetchone()[0]    
    
    query = "UPDATE checkout SET Borrower_ID = ?, Item_ID = ?, Checkout_Date = ?, Due_Date = ?, Closed_Date = ? WHERE ID = ?"
    cur.execute(query, (Borrower_ID, Item_ID, Checkout_Date, Due_Date, Closed_Date, ID))


    # cur.execute("UPDATE checkout SET " + updateIfNotNull.uINN("Borrower_ID", Borrower_ID) + ", " + updateIfNotNull.uINN("Item_ID", Item_ID) + ", " + updateIfNotNull.uINN("Checkout_Date", Checkout_Date) + ", " + updateIfNotNull.uINN("Due_Date", Due_Date) + ", " + updateIfNotNull.uINN("Closed_Date", Closed_Date) + " WHERE ID = " + str(ID))

    # commit changes to db file
    conn.commit()

    # empty table check
    return cur.rowcount > 0