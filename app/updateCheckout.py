import sqlite3

import updateIfNotNull

# connect to the database file
db = sqlite3.connect("database.db")
cur = db.cursor()

# updateCheckout(ID: int, Borrower_ID: int, Item_ID: int, Checkout_Date: str, Due_Date: str, Closed_Date: str):
# updates a checkout item record with given fields in the database
def updateCheckout(conn: Connection, ID: int, Borrower_ID: int, Item_ID: int, Checkout_Date: str, Due_Date: str, Closed_Date: str):
    # set cursor for db interaction
    cur = conn.cursor()

    cur.execute("UPDATE checkout SET " + updateIfNotNull.uINN("Borrower_ID", Borrower_ID) + ", " + updateIfNotNull.uINN("Item_ID", Item_ID) + ", " + updateIfNotNull.uINN("Checkout_Date", Checkout_Date) + ", " + updateIfNotNull.uINN("Due_Date", Dute_Date) + ", " + updateIfNotNull.uINN("Closed_Date", Closed_Date) + " WHERE ID = " + str(ID))

    # commit changes to db file
    conn.commit()