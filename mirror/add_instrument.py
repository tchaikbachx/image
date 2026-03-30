import sys
import sqlite3

def add_instrument(data, conn):
    cur = conn.cursor()
    
    # get the latest ID val w/ guard
    cur.execute("SELECT ID FROM instrument ORDER BY ID DESC LIMIT 1")
    res = cur.fetchone()
    prevID = res[0] if res else 0

    # extract vals from js dict
    new_id = prevID + 1
    name = str(data.get('Name_ID', ''))
    old_id = str(data.get('Old_ID', ''))
    inst_type = str(data.get('Type', ''))
    grade = str(data.get('Grade', ''))
    make = str(data.get('Make', ''))
    model = str(data.get('Model', ''))
    pic = str(data.get('Picture', ''))
    serial = str(data.get('Serial_Number', ''))
    price = str(data.get('Price', '0.0'))
    stored = str(data.get('Stored_In', '0'))
    dept = str(data.get('Dept', '0'))

    # add whatever we just parsed
    query = "INSERT INTO instrument VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    values = (new_id, name, old_id, inst_type, grade, make, model, pic, serial, price, stored, dept)
    
    cur.execute(query, values)
    conn.commit()
    return new_id