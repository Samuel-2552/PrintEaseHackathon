from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
import os

images=os.path.join('static','images')

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['icons'] = images
fav_icon = os.path.join(app.config['icons'], 'logo.png')

def connect_db():
    connection = sqlite3.connect('users.db')
    return connection

@app.route('/')
def index():
    return render_template("index.html", fav_icon=fav_icon)
   

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form['logname']
        password = request.form['logpass']
        email = request.form['logemail']
        connection = connect_db()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cursor.fetchone()
        if user:
            return "User already exists"
        cursor.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", (username, password, email))
        connection.commit()
        connection.close()
        return redirect('/login')
    return render_template('index.html', fav_icon=fav_icon)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form['logemail']
        password = request.form['logpass']
        connection = connect_db()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        if user:
            session['username'] = username
            return redirect('/dashboard')
        return "Invalid username or password"
    return render_template('index.html', fav_icon=fav_icon)

@app.route('/dashboard',methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        # Get the user message from the form
        message = request.form['message']

        # Connect to the database
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        # Update the user message in the database
        cursor.execute('''
        UPDATE users SET message=? WHERE username=?
        ''', (message, session['username']))

        # Commit the changes and close the connection
        conn.commit()
        conn.close()

        # Show a success message
        return 'Message saved successfully'

    # Get the username from the session
    username = session['username']

    # Connect to the database
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Get the user message from the database
    cursor.execute('''
    SELECT message FROM users WHERE username=?
    ''', (username,))
    message = cursor.fetchone()[0]

    # Close the connection
    conn.close()

    # Render the dashboard template with the username and message
    return render_template('dashboard.html', username=username, message=message, fav_icon=fav_icon)

@app.route("/upload-file", methods=["POST"])
def upload_file():
    file = request.files["file"]
    if file and file.content_type == "application/pdf":
        file.save(os.path.join("files", file.filename))
        return "File uploaded successfully!"
    return "No file was provided."

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
