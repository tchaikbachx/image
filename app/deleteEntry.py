import sqlite3

# deleteEntry(table: str, ID: int):
# deletes a row of table `table` with ID `ID`
# it first puts the data into the trashcan table as a backup in case undo is desirable.
def deleteEntry(conn: Connection, table: str, ID: int):
    # set cursor for db interaction
    cur = conn.cursor()

    # add item to the trashcan
    if (table == "locker" or table == "missing" or table == "broken"):
         cur.execute("INSERT INTO trashcan (otherID, col1, col2, col3, col4) SELECT * FROM " + table + " WHERE ID = " + str(ID) + ";")
    if (table == "instrument"):
         cur.execute("INSERT INTO trashcan (otherID, col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, col11) SELECT * FROM instrument WHERE ID = " + str(ID) + ";")
    if (table == "kkey"):
         cur.execute("INSERT INTO trashcan (otherID, col1, col2, col3) SELECT * FROM kkey WHERE ID = " + str(ID) + ";")
    if (table == "borrower" or table == "department"):
         cur.execute("INSERT INTO trashcan (otherID, col1) SELECT * FROM " + table + " WHERE ID = " + str(ID) + ";")
    if (table == "checkout"):
         cur.execute("INSERT INTO trashcan (otherID, col1, col2, col3, col4, col5) SELECT * FROM " + table + " WHERE ID = " + str(ID) + ";")

    # set the trash id and add the table from which the data was grabbed
    prevID = cur.execute("SELECT ID FROM trashcan ORDER BY ID DESC LIMIT 1")
    prevID = cur.fetchone()[0]
    newID = str(prevID + 1 if prevID != None else 1)

    cur.execute("UPDATE trashcan SET ID = " + newID + " WHERE otherID = " + str(ID) + " AND ID is NULL;")
    cur.execute("UPDATE trashcan SET col12 = \'" + str(table) + "\' WHERE ID = " + newID + ";")
    
    # actual deletion:
    cur.execute("DELETE " + table + " WHERE ID = " + str(ID))

    # commit changes to db file
    conn.commit()

    # empty table check
    return cur.rowcount > 0