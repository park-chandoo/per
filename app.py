from flask import Flask, request, render_template_string, jsonify
import sqlite3
import time
import hashlib
import bcrypt

app = Flask(__name__)

# FIXED: SQL Injection vulnerability - using parameterized queries
@app.route('/user/<user_id>')
def get_user(user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # SECURE: Using parameterized query to prevent SQL injection
    try:
        # Validate that user_id is actually an integer
        user_id_int = int(user_id)
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id_int,))
        result = cursor.fetchone()
        conn.close()
        return jsonify(result) if result else jsonify({"error": "User not found"})
    except ValueError:
        conn.close()
        return jsonify({"error": "Invalid user ID format"}), 400

# FIXED: Logic error - corrected fibonacci calculation
@app.route('/calculate/<int:n>')
def calculate_fibonacci(n):
    if n < 0:
        return jsonify({"error": "Invalid input: n must be non-negative"})
    
    # Handle base cases
    if n == 0:
        return jsonify({"fibonacci": 0})
    elif n == 1:
        return jsonify({"fibonacci": 1})
    
    # CORRECTED: Proper fibonacci calculation logic
    fib = [0, 1]
    for i in range(2, n + 1):  # Use range for clearer iteration
        fib.append(fib[i-1] + fib[i-2])
    
    return jsonify({"fibonacci": fib[n]})

# FIXED: Performance issue - using JOIN to eliminate N+1 query problem
@app.route('/users/posts')
def get_users_with_posts():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # OPTIMIZED: Single query using LEFT JOIN to get all data at once
    cursor.execute("""
        SELECT u.id, u.name, p.title 
        FROM users u 
        LEFT JOIN posts p ON u.id = p.user_id 
        ORDER BY u.id, p.id
    """)
    rows = cursor.fetchall()
    
    # Group results by user
    result = []
    current_user = None
    current_posts = []
    
    for row in rows:
        user_id, name, post_title = row
        
        if current_user is None or current_user['id'] != user_id:
            # Save previous user if exists
            if current_user is not None:
                current_user['posts'] = current_posts
                result.append(current_user)
            
            # Start new user
            current_user = {'id': user_id, 'name': name}
            current_posts = []
        
        # Add post if it exists
        if post_title is not None:
            current_posts.append(post_title)
    
    # Don't forget the last user
    if current_user is not None:
        current_user['posts'] = current_posts
        result.append(current_user)
    
    conn.close()
    return jsonify(result)

# FIXED: Secure password hashing using bcrypt
def hash_password(password):
    # SECURE: Using bcrypt with salt for password hashing
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    
    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400
    
    hashed_password = hash_password(password)
    
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                      (username, hashed_password))
        conn.commit()
        return jsonify({"message": "User registered successfully"})
    except sqlite3.IntegrityError:
        return jsonify({"error": "Username already exists"}), 400
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)