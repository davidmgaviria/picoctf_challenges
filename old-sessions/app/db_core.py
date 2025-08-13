import sqlite3
import time
import datetime
import secrets
import os


DB_PATH = "store.db"


# Returns a randomly generated session id
def generate_session_id():
    return secrets.token_hex(16)  


def init_db():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE users (
                username TEXT PRIMARY KEY, 
                password TEXT NOT NULL
            )
        ''')
        c.execute('''
            CREATE TABLE sessions(
                sid TEXT PRIMARY KEY,   
                username TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()


# Add a new user to db
def create_user(username, password) -> bool:
    success = False
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        print("Added (username=%s, password=%s) to user_db" % (username, password))
        success = True
    except sqlite3.IntegrityError as e:
        print(f"IntegrityError: {e}")  # e.g., duplicate key
    except sqlite3.OperationalError as e:
        print(f"OperationalError (connection failed or SQL issue): {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    conn.close()
    return success


def login_user(username, password) -> bool:
    status = False
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username,password))
        row = c.fetchone()
        if row:
            status = True  # get first user (should only be one anyways)
    except sqlite3.OperationalError as e:
        print(f"OperationalError: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    conn.close()
    return status  


def user_exists(username) -> bool:
    status = False
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT username FROM users WHERE username = ?", (username,))
        row = c.fetchone()
        if row:
            status = True  # get first user (should only be one anyways)
    except sqlite3.OperationalError as e:
        print(f"OperationalError: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    conn.close()
    return status  


def get_current_user(sid) -> str:
    user = None
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT username FROM sessions WHERE sid = ?", (sid,))
        row = c.fetchone()
        if row:
            user = row[0]  # get first user (should only be one anyways)
    except sqlite3.OperationalError as e:
        print(f"OperationalError: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    conn.close()
    return user  


