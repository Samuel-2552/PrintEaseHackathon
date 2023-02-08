import sqlite3

# Connect to the database or create it if it doesn't exist
conn = sqlite3.connect('users.db')

# Create a cursor
cursor = conn.cursor()

# Execute a SQL command to create the table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT NOT NULL,
  password TEXT NOT NULL,
  email TEXT NOT NULL,
  message TEXT
)
''')

# Commit the changes and close the connection
conn.commit()
conn.close()
