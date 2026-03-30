import sys
import sqlite3

def delete_instrument(instrument_id, conn):
    cur = conn.cursor()
    # query
    query = "DELETE FROM instrument WHERE ID = ?"
    cur.execute(query, (instrument_id,))
    conn.commit()
    # empty table check
    return cur.rowcount > 0