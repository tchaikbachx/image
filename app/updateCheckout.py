import sys
import sqlite3

import updateIfNotNull

# connect to the database file
db = sqlite3.connect("database.db")
cur = db.cursor()

# updateCheckout(ID: int, Borrower_ID: int, Item_ID: int, Checkout_Date: str, Due_Date: str, Closed_Date: str):
# updates a checkout item record with given fields in the database
def updateCheckout(ID: int, Borrower_ID: int, Item_ID: int, Checkout_Date: str, Due_Date: str, Closed_Date: str):
    cur.execute("UPDATE checkout SET " + updateIfNotNull.uINN("Borrower_ID", Borrower_ID) + ", " + updateIfNotNull.uINN("Item_ID", Item_ID) + ", " + updateIfNotNull.uINN("Checkout_Date", Checkout_Date) + ", " + updateIfNotNull.uINN("Due_Date", Dute_Date) + ", " + updateIfNotNull.uINN("Closed_Date", Closed_Date) + " WHERE ID = " + str(ID))

# call function with passed arguments
updateCheckout(int(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3]), str(sys.argv[4]), str(sys.argv[5]), str(sys.argv[6]))

# commit changes to db file
db.commit()

# close db connection
db.close()