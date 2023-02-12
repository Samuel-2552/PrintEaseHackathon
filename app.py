from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
import os

images=os.path.join('static','images')

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['icons'] = images
fav_icon = os.path.join(app.config['icons'], 'logo.png')
load_img = os.path.join(app.config['icons'], 'printease.gif')

def connect_db():
    connection = sqlite3.connect('users.db')
    return connection

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template("index.html", fav_icon=fav_icon, load_img=load_img)
   

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form['logname']
        password = request.form['logpass']
        email = request.form['logemail']
        phoneno=request.form['lognumber']
        connection = connect_db()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM user WHERE username=?", (username,))
        user = cursor.fetchone()
        if user:
            return "User already exists"
        cursor.execute("INSERT INTO user (username, password, email,phoneno) VALUES (?, ?, ?,?)", (username, password, email,phoneno))
        connection.commit()
        connection.close()
        return redirect('/login')
    return render_template('index.html', fav_icon=fav_icon, load_img=load_img)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        useremail = request.form['logemail']
        password = request.form['logpass']
        connection = connect_db()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM user WHERE email=? AND password=?", (useremail, password))
        user = cursor.fetchone()
        
        if user:
            session['username'] = useremail
            return redirect('/dashboard')
        return "Invalid username or password"
    return render_template('index.html', fav_icon=fav_icon, load_img=load_img)

@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        useremail = request.form['logemail']
        return "Email Sent"
    return render_template('forgot.html', fav_icon=fav_icon, load_img=load_img)

@app.route('/dashboard',methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect('/')
    # Get the username from the session
    useremail = session['username']
    conn = sqlite3.connect('users.db')
    
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM user WHERE email=?",(useremail,))
    username=cursor.fetchone()
    print(username)
    # Close the connection
    conn.close()
    # Connect to the database
    

    # Render the dashboard template with the username and message
    return render_template('dashboard.html', username=username[0], fav_icon=fav_icon, load_img=load_img)

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
