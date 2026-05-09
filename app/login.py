import hashlib
import sqlite3
import os

class LoginManager:
    # login object initialization
    # makes the login db table if it doesn't exist and handles connections
    # for login() and changePassword()
    def __init__(self, db_path):
        self.path = db_path
        # just make sure it exists
        conn = self.get_conn()

        # define cursor
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS pws(username STRING PRIMARY KEY, pass STRING)")
        conn.commit()
        conn.close()


    # get the connection
    def get_conn(self):
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        return conn


    # login(conn: Connection, username: str, pw: str)
    # attempts to login a user with given username, password pair
    # using a connection `conn` to the login database
    def login(self, username, pw):
        conn = self.get_conn()
        cur = conn.cursor()

        hashword = hashlib.sha256(pw.encode("utf-8")).hexdigest()
        # switched to paramaterized queries as sql injection guard
        cur.execute("SELECT username FROM pws WHERE username = ? AND pass = ?", (username, hashword))
        result = cur.fetchone()
        conn.close()
        return result['username'] if result else False
    

    # changePassword(conn: Connection, username: str, pw: str, newpw: str)
    # attempts to change the password of a user with given username, password pair
    # using a connection `conn` to the login database and a new password `newpw`
    def changePassword(self, username, pw, newpw):
        conn = self.get_conn()
        cur = conn.cursor()

        # verify prev pass
        old_hash = hashlib.sha256(pw.encode("utf-8")).hexdigest()
        cur.execute("SELECT username FROM pws WHERE username = ? AND pass = ?", (username, old_hash))
        
        if cur.fetchone():
            # 2. if verified hash new pass & update
            new_hash = hashlib.sha256(newpw.encode("utf-8")).hexdigest()
            cur.execute("UPDATE pws SET pass = ? WHERE username = ?", (new_hash, username))
            conn.commit()
            conn.close()
            return "password change successful"
        else:
            conn.close()
            return "password change failed: username and password did not match"

# -------------------------

# # changePassword(conn: Connection, username: str, pw: str, newpw: str)
# # attempts to change the password of a user with given username, password pair
# # using a connection `conn` to the login database and a new password `newpw`
# def changePassword(conn: Connection, username: str, pw: str, newpw: str):
#     cur = conn.cursor()

#     if login(conn, username, pw):
#         newhashword = hashlib.sha256(newpw.encode("utf-8")).hexdigest()
#         cur.execute("UPDATE pws SET pass = " + newhashword + " WHERE user = " + username + " AND pass = " + hashword)
#         return "password change successful"
#     else:
#         return "password change failed: username and password did not match"
