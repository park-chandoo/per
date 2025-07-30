import sqlite3

def init_database():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Insert some sample users
    cursor.execute('''
        INSERT OR IGNORE INTO users (username, password_hash) VALUES 
        ('admin', '5f4dcc3b5aa765d61d8327deb882cf99'),
        ('user1', '7c4a8d09ca3762af61e59520943dc26494f8941b')
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

if __name__ == '__main__':
    init_database()