import pytest
from app import login

# RUN WITH: python -m pytest test_login.py -v
# RUN EVERYTHING WITH: python -m pytest test_manager.py test_login.py test_server.py -v

@pytest.fixture
def auth(tmp_path):
    db_file = tmp_path / "test_auth.db"
    manager = login.LoginManager(str(db_file))
    return manager

# =================================================================
# AUTHENTICATION
# =================================================================

def test_successful_login_flow(auth):
    auth.create_user("grinnell_staff", "pioneer123")
    assert auth.login("grinnell_staff", "pioneer123") == "grinnell_staff"

def test_failed_login_wrong_password(auth):
    auth.create_user("test_user", "correct_password")
    assert auth.login("test_user", "wrong_password") is False

def test_failed_login_nonexistent_user(auth):
    assert auth.login("ghost_user", "some_password") is False

# =================================================================
# PASSWORD MANAGEMENT/SECURITY
# =================================================================

def test_password_change_success(auth):
    auth.create_user("student", "old_pass")
    success, msg = auth.change_password("student", "old_pass", "new_pass")
    
    assert success is True
    assert auth.login("student", "new_pass") == "student"
    assert auth.login("student", "old_pass") is False

def test_change_password_unauthorized(auth):
    auth.create_user("admin", "super_secret")
    success, msg = auth.change_password("admin", "wrong_current_pass", "hack_attempt")
    
    assert success is False
    assert auth.login("admin", "super_secret") == "admin"
    assert auth.login("admin", "hack_attempt") is False

# =================================================================
# DATAB INTEGRITY + EDGE CASES
# =================================================================

def test_duplicate_user_collision(auth):
    auth.create_user("admin", "pass1")
    
    try:
        auth.create_user("admin", "pass2")
    except Exception:
        pass
        
    assert auth.login("admin", "pass1") == "admin"
    assert auth.login("admin", "pass2") is False

def test_case_sensitivity(auth):
    auth.create_user("StaffMember", "password")    
    result = auth.login("staffmember", "password")

    assert result in ["StaffMember", False]

def test_empty_credentials(auth):
    auth.create_user("", "")
    assert auth.login("", "") == ""