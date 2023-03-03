import sqlite3

# Connect to the database or create it if it doesn't exist
conn = sqlite3.connect('users.db')

# Create a cursor
cursor = conn.cursor()

# Execute a SQL command to create the table
cursor.execute('''
CREATE TABLE IF NOT EXISTS user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT NOT NULL,
  password TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  wallet DECIMAL(1000,2) DEFAULT 0.00,
  EV INTEGER DEFAULT 0,
  otp integer DEFAULT 0
)
''')

# Commit the changes and close the connection
conn.commit()
conn.close()
