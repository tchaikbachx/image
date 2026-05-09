import sqlite3

# input item ID (and table type) to get all things they have had out in the last X years
# ideally will get turned into JSON but idk how to 
# NOTE THAT IT ONLY WORKS ON ITEMS THAT HAVE A TYPE IN THE TABLE...
# example: "getItemHistory.getItemHistory(db, 115, "kkey")"
def getItemHistory(conn: Connection, Item_ID: int, Item_Type: str):

    # set cursor for db interaction
    cur = conn.cursor()

    HistoryList = []

    # grab the item id, item type, checkout date, due date, and closed date (if any) from borrower's row(s)
    query = "SELECT * FROM checkout WHERE Item_ID=? and Item_Type=?"
    for row in cur.execute(query, (Item_ID,Item_Type)):
        HistoryList.append(row)
        # print(row)

    # print(HistoryList)

    return HistoryList