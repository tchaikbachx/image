import sqlite3, sys, os

# ADD
from app.addBorrower import addBorrower as aborr
from app.addBroken import addBroken as abrok
from app.addCheckout import addCheckout as achek
from app.addDepartment import addDepartment as adept
from app.addInstrument import addInstrument as ainst
from app.addKkey import addKkey as akkey
from app.addLocker import addLocker as alock
from app.addMissing import addMissing as amiss

# UPDATE
from app.updateBorrower import updateBorrower as uborr
from app.updateBroken import updateBroken as ubrok
from app.updateCheckout import updateCheckout as uchek
from app.updateDepartment import updateDepartment as udept
from app.updateInstrument import updateInstrument as uinst
from app.updateKkey import updateKkey as ukkey
from app.updateLocker import updateLocker as ulock
from app.updateMissing import updateMissing as umiss

# DELETE/MISC
from app.updateIfNotNull import uINN
from app.deleteEntry import deleteEntry as trash
from app.emptyTrash import emptyTrash as clear

# +------------------------------------------------------+

# does the actual database CRUD work
class manager:
    def __init__(self, db_path):
        self.path = db_path
        # local debugging
        if os.path.exists(self.path):
            print(f"--- DB CONNECTED: {self.path} ({os.path.getsize(self.path)} bytes) ---")
        else:
            print(f"--- WARNING: DB NOT FOUND AT {self.path} ---")

    def get_conn(self):
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        return conn

    # links instruments to checkouts, so can display in/out properly
    def status(self, table_name):
        query = """
            SELECT t.*, 
            (SELECT COUNT(*) FROM checkout WHERE Item_ID = t.ID AND Closed_Date IS NULL) as Loan_Count,
            CASE 
                WHEN m.Item_ID IS NOT NULL AND m.Date_Found IS NULL THEN 'MISSING'
                WHEN b.Item_ID IS NOT NULL AND b.Date_Fixed IS NULL THEN 'BROKEN'
                ELSE 'AVAILABLE'
            END as Availability
            FROM instrument t
            LEFT JOIN missing m ON t.ID = m.Item_ID AND m.Date_Found IS NULL
            LEFT JOIN broken b ON t.ID = b.Item_ID AND b.Date_Fixed IS NULL
        """
        try:
            with self.get_conn() as conn:
                cur = conn.cursor()
                cur.execute(query)
                return [dict(row) for row in cur.fetchall()]
        except sqlite3.OperationalError as e:
            print(f"DATABASE ERROR in status(): {e}")
            return []

    # generic fetch for all tables
    def fetch_all(self, table_name):
        """Generic fetch for non-dashboard tables like 'department' or 'borrower'."""
        with self.get_conn() as conn:
            cur = conn.cursor()
            cur.execute(f"SELECT * FROM {table_name}")
            return [dict(row) for row in cur.fetchall()]

    # generic add for tables
    def add(self, table, data):
        logic_map = {
            'borrower': aborr,
            'broken': abrok,
            'checkout': achek,
            'department': adept,
            'instrument': ainst,
            'kkey': akkey,
            'locker': alock,
            'missing': amiss
        }

        if table not in logic_map:
            raise ValueError(f"No add functions found for: {table}")
        with self.get_conn() as conn:
            return logic_map[table](conn, **data)

    # generic update for tables 
    def update(self, table, entry_id, data):
        logic_map = {
            'borrower': uborr,
            'broken': ubrok,
            'checkout': uchek,
            'department': udept,
            'instrument': uinst,
            'kkey': ukkey,
            'locker': ulock,
            'missing': umiss
        }
        if table not in logic_map:
            raise ValueError(f"No update logic found for: {table}")
        
        with self.get_conn() as conn:
            # id is first arg then trust backend to unpack the rest
            return logic_map[table](conn, entry_id, **data)

    # delete an entry
    def delete(self, table, entry_id):
        with self.get_conn() as conn:
            return trash(conn, table, entry_id)

    # clear the trashcan
    def clear_trash(self):
        with self.get_conn() as conn:
            return clear(conn)