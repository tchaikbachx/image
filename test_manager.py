import pytest
import sqlite3
from manager import manager

# RUN WITH: python -m pytest test_manager.py
# RUN EVERYTHING WITH: python -m pytest test_manager.py test_login.py test_server.py -v

@pytest.fixture
def db(tmp_path):
    db_path = str(tmp_path / "test_inventory.db")
    m = manager(db_path)
    
    with m.get_conn() as conn:
        conn.execute("CREATE TABLE instrument (ID INTEGER PRIMARY KEY, Name_ID TEXT, Locker_ID INTEGER, Key_ID INTEGER)")
        conn.execute("CREATE TABLE locker (ID INTEGER PRIMARY KEY, Kkey INTEGER)")
        conn.execute("CREATE TABLE kkey (ID INTEGER PRIMARY KEY, Name_ID TEXT)")
        conn.execute("CREATE TABLE checkout (ID INTEGER PRIMARY KEY, Item_ID INTEGER, Item_Type TEXT, Borrower_ID TEXT, Closed_Date TEXT)")
        conn.commit()
    return m

# =================================================================
# CORE LOGIC + CASCADING ITEMS
# =================================================================

def test_instrument_return_cascade(db):
    with db.get_conn() as conn:
        conn.execute("INSERT INTO instrument VALUES (101, 'Flute-A', 10, 50)")
        conn.execute("INSERT INTO checkout (ID, Item_ID, Item_Type, Borrower_ID) VALUES (1, 101, 'instrument', 'user@grinnell.edu')")
        conn.execute("INSERT INTO checkout (ID, Item_ID, Item_Type, Borrower_ID) VALUES (2, 10, 'locker', 'user@grinnell.edu')")
        conn.execute("INSERT INTO checkout (ID, Item_ID, Item_Type, Borrower_ID) VALUES (3, 50, 'kkey', 'user@grinnell.edu')")
        conn.commit()

    db.generalized_return(1)

    with db.get_conn() as conn:
        closed = conn.execute("SELECT COUNT(*) FROM checkout WHERE Closed_Date IS NOT NULL").fetchone()[0]
        assert closed == 3

def test_locker_key_return(db):
    with db.get_conn() as conn:
        conn.execute("INSERT INTO locker VALUES (20, 60)")
        conn.execute("INSERT INTO checkout (ID, Item_ID, Item_Type, Borrower_ID) VALUES (4, 20, 'locker', 'user@grinnell.edu')")
        conn.execute("INSERT INTO checkout (ID, Item_ID, Item_Type, Borrower_ID) VALUES (5, 60, 'kkey', 'user@grinnell.edu')")
        conn.commit()

    db.generalized_return(4)

    with db.get_conn() as conn:
        closed = conn.execute("SELECT COUNT(*) FROM checkout WHERE ID = 5 AND Closed_Date IS NOT NULL").fetchone()
        assert closed is not None

# =================================================================
# SECURITY & CRUD
# =================================================================

def test_status_security_whitelist(db):
    """Ensures staff can't accidentally (or maliciously) access unauthorized tables."""
    with pytest.raises(ValueError, match="Invalid table name"):
        db.status("pws")

def test_delete_functionality(db):
    """Verifies that the manager's delete function removes items correctly."""
    with db.get_conn() as conn:
        conn.execute("INSERT INTO instrument (ID, Name_ID) VALUES (999, 'Trash-Oboe')")
        conn.commit()
    
    db.delete('instrument', 999)
    assert len(db.status('instrument')) == 0

# =================================================================
# EDGE CASES
# =================================================================

def test_borrower_isolation(db):
    with db.get_conn() as conn:
        conn.execute("INSERT INTO locker (ID, Kkey) VALUES (30, 70)")
        conn.execute("INSERT INTO checkout (ID, Item_ID, Item_Type, Borrower_ID) VALUES (300, 30, 'locker', 'student_a@grinnell.edu')")
        conn.execute("INSERT INTO checkout (ID, Item_ID, Item_Type, Borrower_ID) VALUES (301, 70, 'kkey', 'student_b@grinnell.edu')")
        conn.commit()

    db.generalized_return(300)

    with db.get_conn() as conn:
        key_loan = conn.execute("SELECT Closed_Date FROM checkout WHERE ID = 301").fetchone()
        assert key_loan['Closed_Date'] is None

def test_history_protection(db):
    with db.get_conn() as conn:
        conn.execute("INSERT INTO checkout (ID, Item_ID, Item_Type, Borrower_ID, Closed_Date) VALUES (80, 101, 'instrument', 'user@grinnell.edu', '2025-12-01')")
        conn.execute("INSERT INTO checkout (ID, Item_ID, Item_Type, Borrower_ID) VALUES (81, 101, 'instrument', 'user@grinnell.edu')")
        conn.commit()

    db.generalized_return(81)

    with db.get_conn() as conn:
        old_date = conn.execute("SELECT Closed_Date FROM checkout WHERE ID = 80").fetchone()[0]
        assert old_date == '2025-12-01'

def test_graceful_missing_links(db):
    """Edge Case: Code should skip links that don't exist in the database."""
    with db.get_conn() as conn:
        conn.execute("INSERT INTO instrument (ID, Locker_ID) VALUES (700, 999)")
        conn.execute("INSERT INTO checkout (ID, Item_ID, Item_Type, Borrower_ID) VALUES (7000, 700, 'instrument', 'user@grinnell.edu')")
        conn.commit()

    assert db.generalized_return(7000) is True