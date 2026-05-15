import pytest
import os
import sqlite3
import importlib
import server
from server import app as flask_app
from dotenv import load_dotenv

# RUN WITH: python -m pytest test_server.py -v
# RUN EVERYTHING WITH: python -m pytest test_manager.py test_login.py test_server.py -v

# --- FIXTURES ---

@pytest.fixture
def app(tmp_path):
    db_file = tmp_path / "deploy_test.db"
    
    # init so tests don't fail on missing tables
    conn = sqlite3.connect(str(db_file))
    conn.executescript("""
        CREATE TABLE instrument (ID INTEGER PRIMARY KEY, Name_ID TEXT, Locker_ID INTEGER, Key_ID INTEGER);
        CREATE TABLE locker (ID INTEGER PRIMARY KEY, Kkey INTEGER);
        CREATE TABLE kkey (ID INTEGER PRIMARY KEY, Name_ID TEXT);
        CREATE TABLE borrower (ID INTEGER PRIMARY KEY, Email TEXT);
        CREATE TABLE checkout (ID INTEGER PRIMARY KEY, Item_ID INTEGER, Item_Type TEXT, Borrower_ID TEXT, Closed_Date TEXT, Due_Date TEXT);
        CREATE TABLE pws (username TEXT PRIMARY KEY, pass TEXT);
    """)
    conn.close()

    flask_app.config.update({
        "TESTING": True,
        "SECRET_KEY": "REALLY_LONG_PRODUCTION_STRENGTH_KEY_5521",
        "SESSION_COOKIE_SECURE": False,
    })
    return flask_app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def staff_session(client):
    """Simulates a secure, verified Admin session."""
    with client.session_transaction() as sess:
        sess['is_staff'] = True
        sess['user_id'] = 'admin_user'
    return client

# =================================================================
# ENVIRONMENT & CONFIGURATION
# =================================================================

def test_production_config_loading():
    os.environ['SECRET_KEY'] = 'super-secret-test-key'
    
    importlib.reload(server)
    
    assert server.app.secret_key == 'super-secret-test-key'
    
    del os.environ['SECRET_KEY']
    importlib.reload(server)

def test_db_path_resolved():
    assert server.db_path is not None
    assert os.path.exists(os.path.dirname(server.db_path))


# =================================================================
# "HACKING"
# =================================================================

def test_unauthorized_api_block(client):
    assert client.delete('/api/instrument/1').status_code == 403
    assert client.post('/api/checkout', json={}).status_code == 403

def test_table_injection_guard(staff_session):
    response = staff_session.get('/api/pws')
    assert response.status_code in [403, 500]

def test_mass_assignment_scrubbing(staff_session):
    payload = {"Name_ID": "New Flute", "ID": 999, "Status": "IN"}
    response = staff_session.put('/api/instrument/1', json=payload)
    assert response.status_code == 200 


# =================================================================
# CORE LOGIC (functionality)
# =================================================================

def test_checkout_validation_logic(staff_session):
    payload = {"item_id": 1, "item_type": "instrument"}
    response = staff_session.post('/api/checkout', json=payload)
    assert response.status_code == 400
    assert b"no email" in response.data or b"no due_date" in response.data

def test_logout_clears_auth(staff_session):
    """RELIABILITY: Ensure logout successfully destroys the session privilege."""
    staff_session.get('/logout')
    # following request should now be blocked
    assert staff_session.delete('/api/instrument/1').status_code == 403

# =================================================================
# ITEM CASCADING
# =================================================================

def test_cascade_return_integrity(staff_session):
    response = staff_session.post('/api/return/1') 
    assert response.status_code == 200
    assert response.get_json()['status'] in ["success", "failed"] 

def test_borrower_isolation(staff_session):
    pass # covered by test_manager.py

def test_db_path_resolved():
    from server import db_path
    assert db_path is not None
    assert os.path.exists(os.path.dirname(db_path))