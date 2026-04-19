import os
import sys
import datetime
import sqlite3

sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

# ADD
from app.addBorrower import addBorrower as aborr
from app.addBroken import addBroken as abrok
from app.addCheckout import addCheckout as achek
from app.addDepartment import addDepartment as adepa
from app.addInstrument import addInstrument as ainst
from app.addKkey import addKkey as akkey
from app.addLocker import addLocker as alock
from app.addMissing import addMissing as amiss

# UPDATE
from app.updateBorrower import updateBorrower as uborr
from app.updateBroken import updateBroken as ubrok
from app.updateCheckout import updateCheckout as uchek
from app.updateDepartment import updateDepartment as udepa
from app.updateInstrument import updateInstrument as uinst
from app.updateKkey import updateKkey as ukkey
from app.updateLocker import updateLocker as ulock
from app.updateMissing import updateMissing as umiss

# DELETE
from app.deleteEntry import deleteEntry

# -----------------------------------------------------------

# separated the function out so that the server is divided from
# the database to meet abstraction goal (and it is cleaner).
class manager:
    def __init__(self, path):
        self.path = path
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
        

    def update(self, table, id, data):
        if table not in self.update_map:
            raise ValueError(f"No update method defined for table: {table}")
        
        with self.get() as conn:
            return self.update_map[table](conn, id, **data)