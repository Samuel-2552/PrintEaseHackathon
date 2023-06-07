from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

DB_NAME = 'login.db'

# Create a table to store user login information
def create_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email  TEXT NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Initialize the database
create_table()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/servicedetails')
def servicedetails():
    return render_template('service-details copy.html')


@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/login')
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Insert the login details into the database
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (email, password) VALUES (?, ?)', (email, password))
        conn.commit()
        conn.close()
        
        return 'Login successful'
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/registerbusiness')
def registerbusiness():
    return render_template('register business.html')


@app.route('/forgot')
def forgot():
    return render_template('forgot-password.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
