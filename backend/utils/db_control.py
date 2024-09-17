import sqlite3
from sqlite3 import Error, Connection

import hashlib

DB_PATH = "backend/database.db"


# Function to create a database connection
def create_connection(db_file=DB_PATH) -> Connection:
    """Creates a database connection to the SQLite database specified by db_file."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


# Function to create the user_data table
def create_table(conn):
    """Creates the user_data table with columns for personal and card information."""
    try:
        user_data_table = """ CREATE TABLE IF NOT EXISTS user_data (
                    Username TEXT,
                    Password TEXT,
                    Email TEXT,
                    Detection_Type TEXT,
                    Video_Tested TEXT,
                    Video_Path TEXT,
                    Results TEXT,
                    UNIQUE(Username, Email)
                ); """

        cur = conn.cursor()
        cur.execute(user_data_table)
    except:
        print("Error: Could not create table user_data")
    conn.close()


# Function to insert data into the table
def append_data(username, detection_type, tested_videos, video_path, results):
    """Inserts multiple rows of data into the user_data table using a prepared statement."""
    try:
        conn = create_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE user_data
            SET Detection_Type = Detection_Type  || ? || ",",
                Video_Tested = Video_Tested  || ? || ",",
                Video_Path = Video_Path  || ? || ",",
                Results = Results  || ? || ","
            WHERE Username = ?;
                """, (detection_type, tested_videos, video_path, results, username))
        conn.commit()
    except:
        print("Error: Could not append new data into user")
    conn.close()

# Function to extract user data by given username
def extract_user_data(username):
    """Extracts user data based on the given username."""
    try:
        conn = create_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT Detection_Type, Video_Tested, Video_Path, Results FROM user_data WHERE Username = ?", (username,))
        data = cursor.fetchall()

         # Convert the fetched data into a dictionary with the username as a key
        result = {
            "data": [dict(zip([col[0] for col in cursor.description], row)) for row in data]
        }
        return result

    except sqlite3.Error as e:
        print("Error:", e)
    finally:
        conn.close()

# Function that returns users password by given username
def get_user_by_username(username):
    """Retrieves a user's username and password based on the provided username."""
    try:
        conn = create_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT password FROM user_data WHERE username = ?", (username,))
        result = cursor.fetchone()

        conn.close()
        return result
    except:
        return None


# Function to hash a password using SHA-256
def hash_func(password):
    """Hashes the provided password using the SHA-256 algorithm."""
    return hashlib.sha256(str(password).encode()).digest()

# Function that uses hash function to compare password from the dataset and the password the user input
def check_password(input_pass, db_pass):
    return hash_func(input_pass) == db_pass[0]

# Function that returns True and False based on if the user input the right credentials 
def authenticate_user(username, password):
    # Check if user exists and password matches
    db_password = get_user_by_username(username)
    if db_password and check_password(password, db_password):
        return True
    return False

# Function that checks if the user already exists
def user_exists(username, email):
    try:
        """Checks if a user exists based on their email address."""
        conn = create_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM user_data WHERE Email = ? OR Username = ?", (email, username))
        count = cursor.fetchone()[0]

        conn.close()
        return count > 0
    except Exception as e:
        print("An Error occurred: ", e)
        return None


# Function to insert data into the table
def insert_data(username, hashed_password, email, detection_type, tested_videos, video_paths, results):
    try:
        """Inserts multiple rows of data into the user_data table using a prepared statement."""
        sql = """ INSERT INTO user_data (Username, Password, Email, Detection_Type , Video_Tested, Video_Path, Results)
                    VALUES (?,?,?,?,?,?,?)"""
        
        conn = create_connection()
        cur = conn.cursor()
        data = [username, hashed_password, email, detection_type, tested_videos, video_paths, results]
        cur.execute(sql, data)
        conn.commit()
    except:
        print("Error: Could not insert new data into user")


# Function that handles registration of the user, by username password and email
def register_user(username, password, email):
    try:
        # Check if user already exists
        if user_exists(username, email):
            return False

        # Hash the password for security
        hashed_password = hash_func(password)
        detection_type = ''
        tested_videos = ''
        video_paths = ''
        results = ''

        # Store user information in the database
        insert_data(username, hashed_password, email, detection_type, tested_videos, video_paths, results)

        return True
    except:
        return None


# Apply the code below only for total reset of the database.
# conn = create_connection()
# cur = conn.cursor()
# cur.execute("DROP TABLE IF EXISTS user_data")
# create_table(conn)
# conn.close()