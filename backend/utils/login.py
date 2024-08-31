from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import hashlib


app = Flask(__name__)

DB_PATH = "backend/database.db"


def get_user_by_username(username):
    """Retrieves a user's username and password based on the provided username."""

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()

    conn.close()
    return result


# Function to hash a password using SHA-256
def hash_func(password):
    """Hashes the provided password using the SHA-256 algorithm."""
    return hashlib.sha256(str(password).encode()).digest()


def check_password(input_pass, db_pass):
    return hash_func(input_pass) == db_pass


def authenticate_user(username, password):
    # Check if user exists and password matches
    user = get_user_by_username(username)
    if user and check_password(password, user[1]):
        return True
    return False


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if authenticate_user(username, password):
            # Redirect to protected area or home page
            return redirect(url_for('protected_area'))
        else:
            # Handle login failure (e.g., incorrect credentials)
            return render_template('login.html', error="Invalid username or password")

    return render_template('login.html')