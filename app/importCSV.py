import sys
import sqlite3
import csv
from tkinter.font import names
import pandas as pd

from exportAsCSV import exportAsCSV

# # # READ ME
#     Column names in the csv file must match the column names in the database tables.
#     Duplicate IDs will cause error
#     HOW TO DEAL WITH UNIQUE IDS for import???
#     will need to ensure that the file is of correct form. 
#     this command should not really be used by users without significant safeguards and checking
#     we should test what happens if the file is not of correct form to see what happens.

# connect to the database file
db = sqlite3.connect("database.db")
cur = db.cursor()

def importCSV(tableName: str):
    df = pd.read_csv("import_file.csv")
    df.to_sql(tableName, db, if_exists='append', index=False)

# call function with passed arguments
importCSV(str(sys.argv[1]))

# commit changes to db file
db.commit() 

# close db connection
db.close()

