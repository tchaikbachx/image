import os
import sys
import datetime
import sqlite3

sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

# ADD
from addBorrower import addBorrower as aborr
from addBroken import addBroken as abrok
from addCheckout import addCheckout as achek
from addDepartment import addDepartment as adepa
from addInstrument import addInstrument as ainst
from addKkey import addKkey as akkey
from addLocker import addLocker as alock
from addMissing import addMissing as amiss

# UPDATE
from updateBorrower import updateBorrower as uborr
from updateBroken import updateBroken as ubrok
from updateCheckout import updateCheckout as uchek
from updateDepartment import updateDepartment as udepa
from updateInstrument import updateInstrument as uinst
from updateKkey import updateKkey as ukkey
from updateLocker import updateLocker as ulock
from updateMissing import updateMissing as umiss

# DELETE
from deleteEntry import deleteEntry

# -----------------------------------------------------------

# separated the function out so that the server is divided from
# the database to meet abstraction goal (and it is cleaner).
class manager:
    def __init__(self, db_path):
        self.path = db_path
        self.add_map = {
            'borrower': aborr,
            'broken': abrok,
            'checkout': achek,
            'department': adepa,
            'instrument': ainst,
            'key': akkey,
            'lock': alock,
            'missing': amiss
        }

        self.update_map = {
            'borrower': uborr,
            'broken': ubrok,
            'checkout': uchek,
            'department': udepa,
            'instrument': uinst,
            'key': ukkey,
            'lock': ulock,
            'missing': umiss
        }


    def get(self):
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        return conn
    

    def fetch(self, table):
        with self.get() as conn:
            cur = conn.cursor()
            cur.execute(f"SELECT * FROM {table}")
            return [dict(row) for row in cur.fetchall()]
        

    def status(self):
        query = """
            SELECT i.*,
            CASE WHEN c.Item_ID IS NOT NULL THEN 'OUT' ELSE 'IN' END as Status
            FROM instrument i
            LEFT JOIN checkout c ON i.Name_ID = c.Item_ID
        """
        with self.get() as conn:
            cur = conn.cursor()
            cur.execute(query)
            return [dict(row) for row in cur.fetchall()]


    def delete(self, table, id):
        with self.get() as conn:
            cur = conn.cursor()
            cur.execute(f"DELETE FROM {table} WHERE ID = ?", (id,))
            conn.commit()
            return cur.rowcount > 0


    def add(self, table, data):
        if table not in self.add_map:
            raise ValueError(f"No add method defined for table: {table}")
        
        with self.get() as conn:
            return self.add_map[table](conn, **data)
        

    def update(self, table, entry_id, data):
        # data dictionary {'Type': 'Horn', 'Make': 'Yamaha'}
        if not data:
            return False

        keys = [f"{k} = ?" for k in data.keys()]
        query = f"UPDATE {table} SET {', '.join(keys)} WHERE ID = ?"
        
        # combine values [value1, value2, ..., entry_id]
        params = list(data.values()) + [entry_id]
        
        with self.get() as conn:
            cur = conn.cursor()
            try:
                cur.execute(query, params)
                conn.commit()
                return cur.rowcount > 0
            except Exception as e:
                # this is for debugging in browser console
                print(f"SQL Error: {query} with params {params}")
                raise e