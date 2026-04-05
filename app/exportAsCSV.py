import sys
import sqlite3
import csv
import pandas as pd

# # READ ME
#     May want a function that turns tables into readable tables
#     i.e. the foreign keys turn into the actual names instead of just the ID numbers

# connect to the database file
db = sqlite3.connect("database.db")
cur = db.cursor()

def exportAsCSV(tableName: str):
    # export the table as a csv file
    # df = pd.read_sql_query("SELECT * FROM " + tableName, db)
    df = pd.read_sql_query("SELECT * FROM borrower", db)
    df.to_csv( "output_file.csv", index=False)


# call function with passed arguments
exportAsCSV(str(sys.argv[1]))

# commit changes to db file
db.commit() 

# close db connection
db.close()

