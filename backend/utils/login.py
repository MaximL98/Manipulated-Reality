import sqlite3
import hashlib

DB_PATH = "backend/database.db"


def get_user_by_username(username):
    """Retrieves a user's username and password based on the provided username."""

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT password FROM user_data WHERE username = ?", (username,))
    result = cursor.fetchone()

    conn.close()
    return result


# Function to hash a password using SHA-256
def hash_func(password):
    """Hashes the provided password using the SHA-256 algorithm."""
    return hashlib.sha256(str(password).encode()).digest()


def check_password(input_pass, db_pass):
    return hash_func(input_pass) == db_pass[0]


def authenticate_user(username, password):
    # Check if user exists and password matches
    db_password = get_user_by_username(username)
    if db_password and check_password(password, db_password):
        return True
    return False
