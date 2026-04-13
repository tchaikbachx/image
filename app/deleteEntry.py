import sqlite3

# connect to the database file
db = sqlite3.connect("database.db")
cur = db.cursor()

# deleteEntry(table: str, ID: int):
# deletes a row of table `table` with ID `ID`
def deleteEntry(conn: Connection, table: str, ID: int):
    # set cursor for db interaction
    cur = conn.cursor()

    cur.execute("DELETE " + table + " WHERE ID = " + str(ID))

    # commit changes to db file
    conn.commit()