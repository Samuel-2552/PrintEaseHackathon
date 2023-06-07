import sqlite3

# Create a connection to the database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create the 'users' table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT NOT NULL,
        password TEXT NOT NULL
    )
''')

# Create the 'businesses' table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS business (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT NOT NULL,
        password TEXT NOT NULL,
        business_name TEXT NOT NULL,
        business_address TEXT NOT NULL,
        business_phone TEXT NOT NULL
    )
''')

# Commit the changes and close the connection
conn.commit()
conn.close()
