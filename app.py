from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
import os
import datetime
import PyPDF2

today = datetime.date.today()
tod_date = today.strftime("%d-%m-%Y")
filepath=''
order_no=1
page=0

images=os.path.join('static','images')

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['icons'] = images
fav_icon = os.path.join(app.config['icons'], 'logo.png')
load_img = os.path.join(app.config['icons'], 'printease.gif')
sam = os.path.join(app.config['icons'], 'samuel.jpg')
sandy = os.path.join(app.config['icons'], 'sandy.jpg')
vejay = os.path.join(app.config['icons'], 'vejayy.jpg')
meena =  os.path.join(app.config['icons'], 'meena1.jpg')


def connect_db():
    connection = sqlite3.connect('users.db')
    return connection

def get_num_pages(file_path):
    pdf_file = open(file_path, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    return len(pdf_reader.pages)

@app.route('/')
def landing():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template("landing.html", fav_icon=fav_icon, load_img=load_img)

@app.route('/aboutus')
def aboutus():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect("/#aboutus")   

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
        try:
            cursor.execute("INSERT INTO user (username, password, email) VALUES (?, ?, ?)", (username, password, email))
            connection.commit()
            connection.close()
        except:
            return "Email-Id already registered!"
        
        return redirect('/login')
    return render_template('index.html', fav_icon=fav_icon, load_img=load_img)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        order_no+=1
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

@app.route("/upload-file", methods=["POST"])
def upload_file():
    global filepath
    file = request.files["file"]
    if file and file.content_type == "application/pdf":
        file.save(os.path.join("files", file.filename))
        filepath=os.path.join("files", file.filename)
        pages=get_num_pages(filepath)
        global page
        page=pages
        print("pages = ", page)
        return "File uploaded successfully!"
    return "No file was provided."


@app.route('/dashboard',methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect('/login')
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

@app.route('/payment',methods=['GET', 'POST'])
def payment():
    return render_template('payment.html', fav_icon=fav_icon, load_img=load_img, order_no=order_no, tod_date=tod_date,pages=page)

# contact page has been added-Meena
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template('contact.html', fav_icon=fav_icon, load_img=load_img)


@app.route('/team', methods=['GET', 'POST'])
def team():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template('team.html', fav_icon=fav_icon, load_img=load_img, sam=sam, sandy=sandy, vejay=vejay, meena=meena)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0")
