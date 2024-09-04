import sqlite3
from sqlite3 import Error, Connection
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
                Results TEXT,
                UNIQUE(Username, Email)
            ); """

    cur = conn.cursor()
    cur.execute(user_data_table)


# Function to insert data into the table
def append_data(username, detection_type, tested_videos, results):
    """Inserts multiple rows of data into the user_data table using a prepared statement."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
          UPDATE user_data
          SET Detection_Type = CONCAT(Detection_Type, ?, ','),
              Video_Tested = CONCAT(Video_Tested, ?, ','),
              Results = CONCAT(Results, ?, ',')
          WHERE Username = ?;
            """, (detection_type, tested_videos, results, username))
    conn.commit()


# Apply the code below only for total reset of the database.
# conn = create_connection()
# cur = conn.cursor()
# cur.execute("DROP TABLE IF EXISTS user_data")
# create_table(conn)
# conn.close()
