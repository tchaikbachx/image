import sqlite3

# connect to the database file
db = sqlite3.connect("database.db")
cur = db.cursor()

# addInstrument(Name_ID: str, Old_ID: str, Type: str, Grade: str, Make: str, Model: str, Picture: str, Serial_Number: str, Price: float, Stored_In: int, Dept: int):
# adds an instrument with given fields to the database
def addInstrument(conn: Connection, Name_ID: str, Old_ID: str, Type: str, Grade: str, Make: str, Model: str, Picture: str, Serial_Number: str, Price: float, Stored_In: int, Dept: int):
    # set cursor for db interaction
    cur = conn.cursor()

    # fetch latest ID to populate the new ID field with
    prevID = cur.execute("SELECT ID FROM instrument ORDER BY ID DESC LIMIT 1")
    prevID = cur.fetchone()[0]

    # str() everything else
    Name_ID = str(Name_ID)
    Old_ID = str(Old_ID)
    Type = str(Type)
    Grade = str(Grade)
    Make = str(Make)
    Model = str(Model)
    Picture = str(Picture)
    Serial_Number = str(Serial_Number)
    Price = str(Price)
    Stored_In = str(Stored_In)
    Dept = str(Dept)
    cur.execute("INSERT INTO instrument VALUES (" + str(prevID + 1 if prevID != None else 1) + ",\'" + Name_ID + "\',\'" + Old_ID + "\',\'" + Type + "\',\'" + Grade + "\',\'" + Make + "\',\'" + Model + "\',\'" + Picture + "\',\'" + Serial_Number + "\'," + Price + "," + Stored_In + "," + Dept + ")")

    # commit changes to db file
    conn.commit()