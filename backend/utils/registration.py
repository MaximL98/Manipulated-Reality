import hashlib
import sqlite3
import json

DB_PATH = "backend/database.db"

# Function to hash a password using SHA-256
def hash_func(password):
    """Hashes the provided password using the SHA-256 algorithm."""
    return hashlib.sha256(str(password).encode()).digest()


def user_exists(email):
    """Checks if a user exists based on their email address."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM user_data WHERE Email = ?", (email,))
    count = cursor.fetchone()[0]

    conn.close()
    return count > 0


# Function to insert data into the table
def insert_data(username, hashed_password, email, detection_type, tested_videos, results):
    """Inserts multiple rows of data into the user_data table using a prepared statement."""
    sql = """ INSERT INTO user_data (Username, Password, Email, Detection_Type , Video_Tested, Results)
                VALUES (?,?,?,?,?,?)"""
    
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    data = [username, hashed_password, email, detection_type, tested_videos, results]
    cur.execute(sql, data)
    conn.commit()

# Replace with your actual database operations
def register_user(username, password, email):
    # Check if user already exists
    if user_exists(email):
        return False

    # Hash the password for security
    hashed_password = hash_func(password)
    detection_type = json.dumps([])
    tested_videos = json.dumps([])
    results = json.dumps([])

    # Store user information in the database
    insert_data(username, hashed_password, email, detection_type, tested_videos, results)

    #return True

