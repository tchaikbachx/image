import sqlite3

import updateIfNotNull

# updateDepartment(ID: int, Department_Name: str):
# updates a department record with given fields in the database
def updateDepartment(conn: Connection, ID: int, Department_Name: str):
    # set cursor for db interaction
    cur = conn.cursor()

    cur.execute("UPDATE department SET " + updateIfNotNull.uINN("Department_Name", Department_Name) + " WHERE ID = " + str(ID))

    # commit changes to db file
    conn.commit()

    # empty table check
    return cur.rowcount > 0