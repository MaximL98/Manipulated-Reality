import sqlite3
from sqlite3 import Error, Connection
import json

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


# Function to insert data into the table
def append_data(username, detection_type, tested_videos, video_path, results):
    """Inserts multiple rows of data into the user_data table using a prepared statement."""
    conn = sqlite3.connect(DB_PATH)
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


# # Example usage:
# username = "c1" 
# user_data = extract_user_data(username)

# # Save the data to a JSON file
# with open("user_data.json", "w") as f:
#     json.dump(user_data, f, indent=4)


# Apply the code below only for total reset of the database.
conn = create_connection()
cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS user_data")
create_table(conn)
conn.close()
