from flask import Flask, request, jsonify, render_template_string, session, redirect, url_for
import sqlite3
import hashlib
import os
import re
from datetime import datetime
import bcrypt

app = Flask(__name__)

# Use environment variable for secret key or generate a secure one
app.secret_key = os.environ.get('SECRET_KEY') or os.urandom(24).hex()

# Bug 2: Global database connection - performance and resource leak issue
db_connection = sqlite3.connect('users.db', check_same_thread=False)

def init_db():
    cursor = db_connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT,
            email TEXT,
            created_at TIMESTAMP
        )
    ''')
    db_connection.commit()

def get_user_by_username(username):
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    return cursor.fetchone()

def hash_password(password):
    # Use bcrypt for secure password hashing with salt
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password, hashed_password):
    # Verify password against bcrypt hash
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

@app.route('/')
def index():
    return '''
    <h1>User Management System</h1>
    <form action="/register" method="post">
        <input type="text" name="username" placeholder="Username" required><br>
        <input type="password" name="password" placeholder="Password" required><br>
        <input type="email" name="email" placeholder="Email" required><br>
        <button type="submit">Register</button>
    </form>
    <hr>
    <form action="/login" method="post">
        <input type="text" name="username" placeholder="Username" required><br>
        <input type="password" name="password" placeholder="Password" required><br>
        <button type="submit">Login</button>
    </form>
    <hr>
    <form action="/search" method="get">
        <input type="text" name="username" placeholder="Search username"><br>
        <button type="submit">Search</button>
    </form>
    <hr>
    <a href="/admin">Admin Panel</a>
    '''

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')
    
    # Bug 5: No input validation - security and logic issue
    if not username or not password:
        return "Username and password are required", 400
    
    hashed_password = hash_password(password)
    
    try:
        cursor = db_connection.cursor()
        cursor.execute(
            'INSERT INTO users (username, password, email, created_at) VALUES (?, ?, ?, ?)',
            (username, hashed_password, email, datetime.now())
        )
        db_connection.commit()
        return "User registered successfully!", 200
    except sqlite3.IntegrityError:
        return "Username already exists", 400

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if not username or not password:
        return "Username and password are required", 400
    
    cursor = db_connection.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    
    if user and verify_password(password, user[2]):  # user[2] is the password field
        return f"Welcome {username}!", 200
    else:
        return "Invalid credentials", 401

@app.route('/search')
def search_user():
    username = request.args.get('username')
    
    if not username:
        return "Username parameter is required", 400
    
    # Bug 6: Using the vulnerable function
    user = get_user_by_username(username)
    
    if user:
        return f"User found: {user[1]} (email: {user[3]})", 200
    else:
        return "User not found", 404

@app.route('/admin')
def admin_panel():
    if not session.get('admin_logged_in'):
        return '''
        <h1>Admin Login</h1>
        <form action="/admin_login" method="post">
            <input type="text" name="username" placeholder="Admin Username" required><br>
            <input type="password" name="password" placeholder="Admin Password" required><br>
            <button type="submit">Login</button>
        </form>
        '''
    
    cursor = db_connection.cursor()
    cursor.execute('SELECT username, email, created_at FROM users')
    users = cursor.fetchall()
    
    user_list = '<br>'.join([f"User: {user[0]}, Email: {user[1]}, Created: {user[2]}" for user in users])
    
    return f'''
    <h1>Admin Panel</h1>
    <a href="/admin_logout">Logout</a>
    <h2>All Users:</h2>
    {user_list}
    '''

@app.route('/admin_login', methods=['POST'])
def admin_login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # Simple admin check - in production, use proper admin authentication
    if username == 'admin' and password == 'admin123':
        session['admin_logged_in'] = True
        return redirect('/admin')
    else:
        return "Invalid admin credentials", 401

@app.route('/admin_logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect('/admin')

if __name__ == '__main__':
    init_db()
    # Use environment variable to control debug mode
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)