import sqlite3, sys, os

# ADD IMPORTS
from app.addBorrower import addBorrower as aborr
from app.addBroken import addBroken as abrok
from app.addCheckout import addCheckout as achek
from app.addDepartment import addDepartment as adept
from app.addInstrument import addInstrument as ainst
from app.addKkey import addKkey as akkey
from app.addLocker import addLocker as alock
from app.addMissing import addMissing as amiss

# UPDATE IMPORTS
from app.updateBorrower import updateBorrower as uborr
from app.updateBroken import updateBroken as ubrok
from app.updateCheckout import updateCheckout as uchek
from app.updateDepartment import updateDepartment as udept
from app.updateInstrument import updateInstrument as uinst
from app.updateKkey import updateKkey as ukkey
from app.updateLocker import updateLocker as ulock
from app.updateMissing import updateMissing as umiss

# DELETE/MISC IMPORTS
from app.updateIfNotNull import uINN
from app.deleteEntry import deleteEntry as trash
from app.emptyTrash import emptyTrash as clear

# +------------------------------------------------------+

# this does the actual database CRUD work
class manager:
    def __init__(self, db_path):
        self.path = db_path
        # [DEBUG] make sure correct database conn is found
        if os.path.exists(self.path):
            print(f"--- DB CONNECTED: {self.path} ({os.path.getsize(self.path)} bytes) ---")
        else:
            print(f"--- WARNING: DB NOT FOUND AT {self.path} ---")


    def get_conn(self):
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        return conn


    # links ALL THE TABLES TO EACHOTHER TO GET THEIR STATUSES. that's it
    def status(self, table_name):
        # determine which table to query
        # >> used names to prevent sql injection since table_name is a string
        valid_tables = ['instrument', 'kkey', 'locker']
        if table_name not in valid_tables:
            return self.fetch_all(table_name)

        # get the item and count active loans
        # >> use subquery for Loan_Count to see if currently OUT
        query = f"""
            SELECT t.*, 
            (SELECT COUNT(*) FROM checkout WHERE Item_ID = t.ID AND Closed_Date IS NULL) as Loan_Count,
            CASE 
        """

        # add specific status for instruments (missing/broken)
        if table_name == 'instrument':
            query = """
                SELECT t.*, 
                    l.Name_ID as Locker_Name,
                    k.Name_ID as Key_Name,
                    (SELECT COUNT(*) FROM checkout 
                    WHERE Item_ID = t.ID AND Item_Type = 'instrument' AND Closed_Date IS NULL) as Loan_Count,
                    CASE 
                        WHEN m.Item_ID IS NOT NULL AND m.Date_Found IS NULL THEN 'MISSING'
                        WHEN b.Item_ID IS NOT NULL AND b.Date_Fixed IS NULL THEN 'BROKEN'
                        WHEN (SELECT COUNT(*) FROM checkout 
                            WHERE Item_ID = t.ID AND Item_Type = 'instrument' AND Closed_Date IS NULL) > 0 THEN 'OUT'
                        ELSE 'AVAILABLE'
                    END as Availability
                FROM instrument t
                LEFT JOIN locker l ON t.Stored_In = l.ID
                LEFT JOIN kkey k ON l.Kkey = k.ID
                LEFT JOIN missing m ON t.ID = m.Item_ID AND m.Date_Found IS NULL
                LEFT JOIN broken b ON t.ID = b.Item_ID AND b.Date_Fixed IS NULL
            """
        # locker table case
        elif table_name == 'locker':
            query = """
                SELECT t.*, 
                    k.Name_ID as Key_Name,
                    (SELECT COUNT(*) FROM checkout 
                    WHERE Item_ID = t.ID AND Item_Type = 'locker' AND Closed_Date IS NULL) as Loan_Count,
                    CASE 
                        WHEN t.Checkoutable = 0 THEN 'RESTRICTED'
                        WHEN (SELECT COUNT(*) FROM checkout 
                            WHERE Item_ID = t.ID AND Item_Type = 'locker' AND Closed_Date IS NULL) > 0 THEN 'OUT'
                        ELSE 'AVAILABLE'
                    END as Availability
                FROM locker t
                LEFT JOIN kkey k ON t.Kkey = k.ID
            """
        # kkey table case
        else:
            query = f"""
                SELECT t.*, 
                    (SELECT COUNT(*) FROM checkout 
                    WHERE Item_ID = t.ID AND Item_Type = 'kkey' AND Closed_Date IS NULL) as Loan_Count,
                    CASE 
                        WHEN (SELECT COUNT(*) FROM checkout 
                            WHERE Item_ID = t.ID AND Item_Type = 'kkey' AND Closed_Date IS NULL) > 0 THEN 'OUT'
                        ELSE 'AVAILABLE'
                    END as Availability
                FROM kkey t
            """

        try:
            with self.get_conn() as conn:
                cur = conn.cursor()
                cur.execute(query)
                return [dict(row) for row in cur.fetchall()]
        except sqlite3.OperationalError as e:
            print(f"DATABASE ERROR in status() for {table_name}: {e}")
            return []


    # helper to get the human-readable Name_ID for a checkout email
    def get_name_by_type(self, item_type, item_id):
        # denote valid tables to prevent injection
        valid_tables = ['instrument', 'kkey', 'locker']
        if item_type not in valid_tables:
            return "Unknown Item"

        try:
            with self.get_conn() as conn:
                cur = conn.cursor()
                # query specific table for Name_ID column using ID
                cur.execute(f"SELECT Name_ID FROM {item_type} WHERE ID = ?", (item_id,))
                result = cur.fetchone()
                return result['Name_ID'] if result else "Unknown Item"
        except Exception as e:
            print(f"Error fetching item name: {e}")
            return "Unknown Item"
        

    # update signature and the INSERT query
    def add_checkout(self, item_id, email, due_date, item_type):
        from datetime import date
        today = date.today().isoformat()
        
        try:
            with self.get_conn() as conn:
                cur = conn.cursor()
                
                # align the borrower and ID counter since it kept double counting
                cur.execute("SELECT ID FROM borrower WHERE Email = ?", (email,))
                borrower = cur.fetchone()
                borrower_id = aborr(conn, email) if not borrower else borrower['ID']
                
                cur.execute("SELECT ID FROM checkout ORDER BY ID DESC LIMIT 1")
                last_row = cur.fetchone()
                current_id_counter = 1 if last_row is None else last_row[0] + 1

                insert_query = """
                    INSERT INTO checkout (ID, Borrower_ID, Item_ID, Item_Type, Checkout_Date, Due_Date)
                    VALUES (?, ?, ?, ?, ?, ?)
                """

                cur.execute(insert_query, (current_id_counter, borrower_id, item_id, item_type, today, due_date))
                
                # this is where it gets annoying to coordinate the updating correctly
                # >> case 1: instrument -> locker -> key
                if item_type == 'instrument':
                    cur.execute("SELECT Stored_In FROM instrument WHERE ID = ?", (item_id,))
                    instr = cur.fetchone()
                    if instr and instr['Stored_In']:
                        locker_id = instr['Stored_In']
                        cur.execute("SELECT Kkey FROM locker WHERE ID = ?", (locker_id,))
                        lock_row = cur.fetchone()
                        
                        # auto-checkout locker (if it exists)
                        current_id_counter += 1
                        cur.execute(insert_query, (current_id_counter, borrower_id, locker_id, 'locker', today, due_date))
                        
                        # auto-checkout key (if it exists)
                        if lock_row and lock_row['Kkey']:
                            current_id_counter += 1
                            cur.execute(insert_query, (current_id_counter, borrower_id, lock_row['Kkey'], 'kkey', today, due_date))

                # >> case 2: locker -> key
                elif item_type == 'locker':
                    cur.execute("SELECT Kkey FROM locker WHERE ID = ?", (item_id,))
                    lock_row = cur.fetchone()
                    if lock_row and lock_row['Kkey']:
                        current_id_counter += 1
                        cur.execute(insert_query, (current_id_counter, borrower_id, lock_row['Kkey'], 'kkey', today, due_date))

                # >> case 3: key -> locker
                elif item_type == 'kkey':
                    cur.execute("SELECT ID FROM locker WHERE Kkey = ?", (item_id,))
                    locker = cur.fetchone()
                    if locker:
                        current_id_counter += 1
                        cur.execute(insert_query, (current_id_counter, borrower_id, locker['ID'], 'locker', today, due_date))

                conn.commit()
                return True
                    
        except Exception as e:
            print(f"Checkout Error: {e}")
            return False
    

    # generic fetch for all tables
    def fetch_all(self, table_name):
        """Generic fetch for non-dashboard tables like 'department' or 'borrower'."""
        with self.get_conn() as conn:
            cur = conn.cursor()
            cur.execute(f"SELECT * FROM {table_name}")
            return [dict(row) for row in cur.fetchall()]


    # generic add for tables
    def add(self, table, data):
        # these map the backend functions to an alias
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
        # these map the backend functions to an alias
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
            raise ValueError(f"No update functions found for: {table}")
        
        with self.get_conn() as conn:
            # id is first arg then trust backend to unpack the rest
            return logic_map[table](conn, entry_id, **data)


    # delete an entry
    def delete(self, table, entry_id):
        with self.get_conn() as conn:
            return trash(conn, table, entry_id)


    # check-in an item (instrument/key/locker) and more really annoying coordination
    def generalized_return(self, checkout_id):
        from datetime import date
        today = date.today().isoformat()
        
        try:
            with self.get_conn() as conn:
                cur = conn.cursor()
                
                # look up the item being returned
                cur.execute("SELECT Item_ID, Item_Type, Borrower_ID FROM checkout WHERE ID = ?", (checkout_id,))
                current_checkout = cur.fetchone()
                
                if not current_checkout:
                    return False

                # close the primary checkout
                uchek(conn, ID=checkout_id, Closed_Date=today)

                item_id = current_checkout['Item_ID']
                item_type = current_checkout['Item_Type']
                borrower_id = current_checkout['Borrower_ID']

                # handle the "twin" returning
                items_to_return = [] # list of (id, type) tuples

                if item_type == 'instrument':
                    # >> case 1: instrument -> locker -> key
                    cur.execute("""
                        SELECT l.ID as Locker_ID, l.Kkey as Key_ID 
                        FROM instrument i
                        LEFT JOIN locker l ON i.Stored_In = l.ID
                        WHERE i.ID = ?
                    """, (item_id,))
                    links = cur.fetchone()
                    if links:
                        if links['Locker_ID']: items_to_return.append((links['Locker_ID'], 'locker'))
                        if links['Key_ID']: items_to_return.append((links['Key_ID'], 'kkey'))

                elif item_type == 'locker':
                    # >> case 2: locker -> key
                    cur.execute("SELECT Kkey FROM locker WHERE ID = ?", (item_id,))
                    locker_row = cur.fetchone()
                    if locker_row and locker_row['Kkey']:
                        items_to_return.append((locker_row['Kkey'], 'kkey'))
                
                elif item_type == 'kkey':
                    # >> case 3: key -> locker
                    cur.execute("SELECT ID FROM locker WHERE Kkey = ?", (item_id,))
                    locker = cur.fetchone()
                    if locker:
                        items_to_return.append((locker['ID'], 'locker'))

                # close all twin checkouts for the SAME borrower
                for twin_id, twin_type in items_to_return:
                    cur.execute("""
                        UPDATE checkout 
                        SET Closed_Date = ? 
                        WHERE Item_ID = ? AND Item_Type = ? 
                        AND Borrower_ID = ? AND Closed_Date IS NULL
                    """, (today, twin_id, twin_type, borrower_id))

                conn.commit()
                return True
                    
        except Exception as e:
            print(f"Return Error: {e}")
            return False


    # clear the trashcan
    def clear_trash(self):
        with self.get_conn() as conn:
            return clear(conn)