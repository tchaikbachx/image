import sqlite3

# input borrower ID to get all things they have had out in the last X years
# ideally will get turned into JSON but idk how to 
# example call: "getBorrowerHistory.getBorrowerHistory(db, 14)"
def getBorrowerHistory(conn: Connection, borrower_ID: int):

    # set cursor for db interaction
    cur = conn.cursor()

    HistoryList = []

    # grab the item id, item type, checkout date, due date, and closed date (if any) from borrower's row(s)
    query = "SELECT * FROM checkout WHERE borrower_ID=?"
    for row in cur.execute(query, (borrower_ID,)):
        HistoryList.append(row)
        # print(row)

    # print(HistoryList)

    return HistoryList