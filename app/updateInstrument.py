import sqlite3

import updateIfNotNull

# updateInstrument(ID: int, Name_ID: str, Old_ID: str, Type: str, Grade: str, Make: str, Model: str, Picture: str, Serial_Number: str, Price: float, Stored_In: int, Dept: int)
# updates an instrument record with given fields in the database
def updateInstrument(conn: Connection, ID: int, Name_ID: str, Old_ID: str, Type: str, Grade: str, Make: str, Model: str, Picture: str, Serial_Number: str, Price: float, Stored_In: int, Dept: int):
    # set cursor for db interaction
    cur = conn.cursor()

    cur.execute("UPDATE instrument SET " + updateIfNotNull.uINN("Name_ID", Name_ID) + ", " + updateIfNotNull.uINN("Old_ID", Old_ID) + ", " + updateIfNotNull.uINN("Type", Type) + ", " + updateIfNotNull.uINN("Grade", Grade) + ", " + updateIfNotNull.uINN("Make", Make) + ", " + updateIfNotNull.uINN("Model", Model) + ", " + updateIfNotNull.uINN("Picture", Picture) + ", " + updateIfNotNull.uINN("Serial_Number", Serial_Number) + ", " + updateIfNotNull.uINN("Price", Price) + ", " + updateIfNotNull.uINN("Stored_In", Stored_In) + ", " + updateIfNotNull.uINN("Dept", Dept) + " WHERE ID = " + str(ID))

    # commit changes to db file
    conn.commit()

    # empty table check
    return cur.rowcount > 0