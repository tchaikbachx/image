import sqlite3

# connect to the database file
db = sqlite3.connect("database.db")
cur = db.cursor()

# addKkey(Name_ID: str, Qty: int, Description: str):
# adds a kkey with given fields to the database
# the description field is for any additional information about the kkey, such as what it opens or where it is stored
def addKkey(conn: Connection, Name_ID: str, Qty: int, Description: str):
    # set cursor for db interaction
    cur = conn.cursor()

    # fetch latest ID to populate the new ID field with
    prevID = cur.execute("SELECT ID FROM kkey ORDER BY ID DESC LIMIT 1")
    prevID = cur.fetchone()[0]

    # str() everything else
    Name_ID = str(Name_ID)
    Qty = str(Qty)
    Description = str(Description)
    cur.execute("INSERT INTO kkey VALUES (" + str(prevID + 1 if prevID != None else 1) + ",\'" + Name_ID + "\'," + Qty + ",\'" + Description + "\')")

    # commit changes to db file
    conn.commit()