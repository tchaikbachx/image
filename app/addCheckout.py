import sys
import sqlite3
import datetime

# connect to the database file
db = sqlite3.connect("database.db")
cur = db.cursor()

# addCheckout(Borrower_ID: int, Item_ID: int, Due_Date: str):
# adds a checkout record with given fields to the database
def addCheckout(Borrower_ID: int, Item_ID: int, Due_Date: str):
    # fetch latest ID to populate the new ID field with
    prevID = cur.execute("SELECT ID FROM checkout ORDER BY ID DESC")
    prevID = cur.fetchone()[0]

    # str() everything else
    Borrower_ID = str(Borrower_ID)
    Item_ID = str(Item_ID)
    Checkout_Date = str(datetime.date.today)
    cur.execute("INSERT INTO checkout VALUES (" + str(prevID + 1 if prevID != None else 1) + "," + Borrower_ID + "," + Item_ID + ",\'" + Checkout_Date + "\',\'" + Due_Date + "\',\'" + "N/A" + "\')")

# call function with passed arguments
addCheckout(int(sys.argv[1]), int(sys.argv[2]), str(sys.argv[3]))

# commit changes to db file
db.commit()

# close db connection
db.close()