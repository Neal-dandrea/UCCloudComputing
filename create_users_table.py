import sqlite3

# Connect to the SQLite database (creates one if not exists)
conn = sqlite3.connect('users.db')
cur = conn.cursor()

# Create 'users' table
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    firstname TEXT,
    lastname TEXT,
    email TEXT,
    address TEXT
)
""")

conn.commit()
conn.close()

print("Users table created successfully!")
