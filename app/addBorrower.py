import sqlite3

def addBorrower(conn, Email: str):
    # set cursor for db interaction
    cur = conn.cursor()

    # 1. Fetch latest ID to populate the new ID field
    cur.execute("SELECT ID FROM borrower ORDER BY ID DESC LIMIT 1")
    result = cur.fetchone()
    
    # Handle empty table case (NoneType check)
    if result is None:
        newID = 1
    else:
        newID = result[0] + 1

    # 2. Insert into the 2 columns your table actually has: ID and Email
    # We use ? placeholders for security and to handle the str() conversion
    query = "INSERT INTO borrower (ID, Email) VALUES (?, ?)"
    cur.execute(query, (newID, str(Email)))

    # commit changes to db file
    conn.commit()

    return newID