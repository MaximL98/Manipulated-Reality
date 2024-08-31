from flask import Flask, render_template, request, redirect, url_for
import hashlib
import sqlite3
import json

app = Flask(__name__)

DB_PATH = "backend/database.db"

# Function to hash a password using SHA-256
def hash_func(password):
    """Hashes the provided password using the SHA-256 algorithm."""
    return hashlib.sha256(str(password).encode()).digest()


def user_exists(email):
    """Checks if a user exists based on their email address."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM users WHERE Email = ?", (email,))
    count = cursor.fetchone()[0]

    conn.close()
    return count > 0


# Function to insert data into the table
def insert_data(conn, data):
    """Inserts multiple rows of data into the user_data table using a prepared statement."""
    sql = """ INSERT INTO user_data (Username, Password, Email, Tested_Videos, Results)
                VALUES (?,?,?,?,?)"""
    
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    for person in data:
        cur.execute(sql, person)
    conn.commit()

# Replace with your actual database operations
def register_user(username, password, email):
    # Check if user already exists
    if user_exists(email):
        return False

    # Hash the password for security
    hashed_password = hash_func(password)
    tested_videos = json.dumps([])
    results = json.dumps([])

    # Store user information in the database
    insert_data(username, hashed_password, email, tested_videos, results)

    return True

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        if register_user(username, password, email):
            return redirect(url_for('login'))  # Redirect to login page after successful registration
        else:
            # Handle registration failure (e.g., user already exists)
            return render_template('register.html', error="Username already exists")

    return render_template('register.html')