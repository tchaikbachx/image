import sys
import sqlite3

import updateIfNotNull

# connect to the database file
db = sqlite3.connect("database.db")
cur = db.cursor()

# updateInstrument(ID: int, Name_ID: str, Old_ID: str, Type: str, Grade: str, Make: str, Model: str, Picture: str, Serial_Number: str, Price: float, Stored_In: int, Dept: int)
# updates an instrument record with given fields in the database
def updateInstrument(ID: int, Name_ID: str, Old_ID: str, Type: str, Grade: str, Make: str, Model: str, Picture: str, Serial_Number: str, Price: float, Stored_In: int, Dept: int):
    cur.execute("UPDATE instrument SET " + updateIfNotNull.uINN("Name_ID", Name_ID) + ", " + updateIfNotNull.uINN("Old_ID", Old_ID) + ", " + updateIfNotNull.uINN("Type", Type) + ", " + updateIfNotNull.uINN("Grade", Grade) + ", " + updateIfNotNull.uINN("Make", Make) + ", " + updateIfNotNull.uINN("Model", Model) + ", " + updateIfNotNull.uINN("Picture", Picture) + ", " + updateIfNotNull.uINN("Serial_Number", Serial_Number) + ", " + updateIfNotNull.uINN("Price", Price) + ", " + updateIfNotNull.uINN("Stored_In", Stored_In) + ", " + updateIfNotNull.uINN("Dept", Dept) + " WHERE ID = " + str(ID))

# call function with passed arguments
updateInstrument(int(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3]), str(sys.argv[4]), str(sys.argv[5]), int(sys.argv[6]), str(sys.argv[7]), str(sys.argv[8]), str(sys.argv[9]), float(sys.argv[10]), int(sys.argv[11]), int(sys.argv[12]))

# commit changes to db file
db.commit()

# close db connection
db.close()