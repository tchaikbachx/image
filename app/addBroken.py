import sqlite3
import datetime

# addBroken(Item_ID: int, Description: str):
# adds a broken item record with given fields to the database
def addBroken(conn: Connection, Item_ID: int, Description: str):
    # set cursor for db interaction
    cur = conn.cursor()

    # fetch latest ID to populate the new ID field with
    prevID = cur.execute("SELECT ID FROM broken ORDER BY ID DESC LIMIT 1")
    prevID = cur.fetchone()[0]
    newID = str(prevID + 1 if prevID != None else 1)

    # str() everything else
    Date_Broken = str(datetime.date.today)
    Item_ID = str(Item_ID)
    Description = str(Description)
    cur.execute("INSERT INTO broken VALUES (" + newID + ",\'" + Date_Broken + "\',\'" + "N/A" + "\'," + Item_ID + ",\'" + Description + "\')")
    
    # commit changes to db file
    conn.commit()

    return newID