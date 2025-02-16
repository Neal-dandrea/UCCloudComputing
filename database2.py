import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('users.db')
cur = conn.cursor()

# Create users table
cur.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    firstname TEXT,
    lastname TEXT,
    email TEXT,
    address TEXT
)
''')

conn.commit()
conn.close()
