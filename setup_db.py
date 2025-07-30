import sqlite3

def setup_database():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            name TEXT
        )
    ''')
    
    # Create posts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT NOT NULL,
            content TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Insert sample data
    sample_users = [
        (1, 'alice', 'hashed_password', 'Alice Smith'),
        (2, 'bob', 'hashed_password', 'Bob Johnson'),
        (3, 'charlie', 'hashed_password', 'Charlie Brown')
    ]
    
    cursor.execute("DELETE FROM users")  # Clear existing data
    cursor.executemany("INSERT INTO users (id, username, password, name) VALUES (?, ?, ?, ?)", sample_users)
    
    sample_posts = [
        (1, 'First Post'),
        (1, 'Second Post'),
        (2, 'Bob\'s Post'),
        (3, 'Charlie\'s Thoughts'),
        (3, 'Another Post by Charlie')
    ]
    
    cursor.execute("DELETE FROM posts")  # Clear existing data
    cursor.executemany("INSERT INTO posts (user_id, title) VALUES (?, ?)", sample_posts)
    
    conn.commit()
    conn.close()
    print("Database setup complete!")

if __name__ == '__main__':
    setup_database()