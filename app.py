from flask import Flask, request, jsonify, render_template_string
import sqlite3
import hashlib
import os
import re
from datetime import datetime
import bcrypt

app = Flask(__name__)

# Fixed: Secure secret key generation
app.secret_key = os.environ.get('SECRET_KEY') or os.urandom(24).hex()

# Fixed: SQL injection vulnerability
def get_user_by_id(user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # FIXED: Using parameterized query to prevent SQL injection
    query = "SELECT * FROM users WHERE id = ?"
    cursor.execute(query, (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

# Fixed: Secure password hashing
def hash_password(password):
    # FIXED: Using bcrypt with salt for secure password hashing
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(password, hashed_password):
    # Helper function to verify passwords
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

@app.route('/')
def index():
    return render_template_string('''
        <html>
            <head><title>User Management</title></head>
            <body>
                <h1>User Management System</h1>
                <form method="POST" action="/login">
                    <input type="text" name="username" placeholder="Username">
                    <input type="password" name="password" placeholder="Password">
                    <button type="submit">Login</button>
                </form>
                <form method="POST" action="/register">
                    <input type="text" name="username" placeholder="Username">
                    <input type="password" name="password" placeholder="Password">
                    <button type="submit">Register</button>
                </form>
                <form method="GET" action="/user">
                    <input type="text" name="id" placeholder="User ID">
                    <button type="submit">Get User</button>
                </form>
            </body>
        </html>
    ''')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # Bug 4: No input validation
    if username and password:
        hashed_password = hash_password(password)
        # Check credentials (simplified)
        return jsonify({"message": "Login successful"})
    return jsonify({"error": "Invalid credentials"})

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # Bug 5: Weak password validation
    if len(password) >= 3:  # Too weak!
        hashed_password = hash_password(password)
        # Save user (simplified)
        return jsonify({"message": "Registration successful"})
    return jsonify({"error": "Password too short"})

@app.route('/user')
def get_user():
    user_id = request.args.get('id')
    if user_id:
        user = get_user_by_id(user_id)
        return jsonify({"user": user})
    return jsonify({"error": "No user ID provided"})

@app.route('/search')
def search_users():
    query = request.args.get('q', '')
    
    # FIXED: Efficient database-level search
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # Use database-level filtering with LIKE operator
    cursor.execute("SELECT * FROM users WHERE username LIKE ?", (f'%{query}%',))
    results = cursor.fetchall()
    conn.close()
    
    return jsonify({"results": results})

if __name__ == '__main__':
    # Fixed: Production-safe configuration
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)