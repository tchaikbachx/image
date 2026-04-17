import sqlite3

# addToTrash(conn: Connection, Name_ID, col1, col2, col3, col4, col5, col6, col 7, col8, col9, col10, col11, col12):
# adds a row to the trash can with given fields to the database
# 
def emptyTrash(conn: Connection):
    # set cursor for db interaction
    cur = conn.cursor()

    # delete all from trashcan
    cur.execute("DELETE FROM trashcan;")

    # add one row of zeros (helps with indexing)
    cur.execute("INSERT INTO trashcan VALUES (0,0,0,0,0,0,0,0,0,0,0,0,0,0);")
   
    # commit changes to db file
    conn.commit()

    return 0