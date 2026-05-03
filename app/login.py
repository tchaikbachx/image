import hashlib
import sqlite3

# login object initialization
# makes the login db table if it doesn't exist and handles connections
# for login() and changePassword()
def __init__(self, db_path):
    self.path = db_path
    # [DEBUG] make sure correct database conn is found
    if os.path.exists(self.path):
        print(f"--- DB CONNECTED: {self.path} ({os.path.getsize(self.path)} bytes) ---")
        cur.execute("CREATE TABLE IF NOT EXISTS pws(STRING username PRIMARY KEY, STRING pass)")
    else:
        print(f"--- WARNING: DB NOT FOUND AT {self.path} ---")

    def get_conn(self):
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        return conn

# login(conn: Connection, username: str, pw: str)
# attempts to login a user with given username, password pair
# using a connection `conn` to the login database
def login(conn: Connection, username: str, pw: str):
    cur = conn.cursor()

    hashword = hashlib.sha256(pw.encode("utf-8")).hexdigest()
    password = cur.execute("SELECT user FROM pws WHERE user = " + username + " AND pass = " + hashword)
    result = cur.fetchone()
    return result['user'] if result else False

# changePassword(conn: Connection, username: str, pw: str, newpw: str)
# attempts to change the password of a user with given username, password pair
# using a connection `conn` to the login database and a new password `newpw`
def changePassword(conn: Connection, username: str, pw: str, newpw: str):
    cur = conn.cursor()

    if login(conn, username, pw):
        newhashword = hashlib.sha256(newpw.encode("utf-8")).hexdigest()
        cur.execute("UPDATE pws SET pass = " + newhashword + " WHERE user = " + username + " AND pass = " + hashword)
        return "password change successful"
    else:
        return "password change failed: username and password did not match"
