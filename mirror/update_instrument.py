import sys
import sqlite3

def update_instrument(instrument_id, data, conn):
    cur = conn.cursor()
    # query pre-existing fields
    query = """
        UPDATE instrument 
        SET Name_ID=?, Old_ID=?, Type=?, Grade=?, Make=?, Model=?, 
            Picture=?, Serial_Number=?, Price=?, Stored_In=?, Dept=?
        WHERE ID=?
    """
    # update with new info entered 
    values = (
        str(data.get('Name_ID', '')), str(data.get('Old_ID', '')),
        str(data.get('Type', '')), str(data.get('Grade', '')),
        str(data.get('Make', '')), str(data.get('Model', '')),
        str(data.get('Picture', '')), str(data.get('Serial_Number', '')),
        float(data.get('Price', 0)), int(data.get('Stored_In', 0)),
        int(data.get('Dept', 0)), instrument_id
    )
    cur.execute(query, values)
    conn.commit()
    # empty table check
    return cur.rowcount > 0