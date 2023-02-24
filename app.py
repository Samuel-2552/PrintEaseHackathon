from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
import os
import datetime
import PyPDF2
import qrcode
import uuid
import math
import random
import smtplib
import imghdr

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

ip="http://192.168.1.10:5000"

qr_codes={}
navbar_name=['GET STARTED','ORDER NOW']
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
qr_img=os.path.join(app.config['icons'], 'qr.png')

def OTP():
    digits = "0123456789"
    OTP = ""
    for i in range(6):
        OTP += digits[math.floor(random.random() * 10)]
    return OTP

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
        logout=1
        email=session['username']
        connection = connect_db()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM user WHERE email=?", (email,))
        user = cursor.fetchone()
        user=user[1][0]
        name=navbar_name[1]
        cursor.execute("SELECT wallet FROM user WHERE email=?", (email,))
        wallet_money=cursor.fetchone()
    else:
        wallet_money=[0]
        logout=0
        user="-1"
        name=navbar_name[0]
        #return redirect(url_for('dashboard'))
    return render_template("landing.html", fav_icon=fav_icon, load_img=load_img,logout=logout,user=user.upper(),ip=ip,name=name,wallet=wallet_money[0])

@app.route('/aboutus')
def aboutus():
    #return redirect(url_for('dashboard'))
    return redirect("/#aboutus")   

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
        cursor.execute("SELECT * FROM user WHERE username=?", (username,))
        user = cursor.fetchone()
        print(user)
        if user:
            return "User already exists"
        try:
            cursor.execute("INSERT INTO user (username, password, email) VALUES (?, ?, ?)", (username, password, email))
            connection.commit()
            connection.close()
        except:
            return "Email-Id already registered!"
        
        return redirect('/login')
    return render_template('index.html', fav_icon=fav_icon, load_img=load_img,ip=ip)

@app.route('/login', methods=['GET', 'POST'])
def login():
    global order_no
    if 'username' in session:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        try:
            useremail = request.form['logemail']
            password = request.form['logpass']
            connection = connect_db()
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM user WHERE email=? AND password=?", (useremail, password))
            user = cursor.fetchone()
            print(user[5])
        except:
            return "Invalid username or password"
        if user:
            session['username'] = useremail
            if user[5]==0:
                print("going")
                return redirect('/verification')
            order_no+=1
            return redirect('/dashboard')
        return "Invalid username or password"
    return render_template('index.html', fav_icon=fav_icon, load_img=load_img,ip=ip)

@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        useremail = request.form['logemail']
        return "Email Sent"
    return render_template('forgot.html', fav_icon=fav_icon, load_img=load_img, ip=ip)

@app.route("/upload-file", methods=["POST"])
def upload_file():
    global filepath
    global page
    file = request.files["file"]
    if file and file.content_type == "application/pdf":
        file.save(os.path.join("files", file.filename))
        filepath=os.path.join("files", file.filename)
        pages=get_num_pages(filepath)
        
        page=pages
        print("pages = ", page)
        return "File uploaded successfully!"
    if imghdr.what(file) is not None:
        file.save(os.path.join("files", file.filename))
        filepath=os.path.join("files", file.filename)
        
        page=1
        return "File uploaded successfully!"
    return "It is not a pdf file"


@app.route('/dashboard',methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        name=navbar_name[0]
        return redirect('/login')
    # Get the username from the session
    useremail = session['username']
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM user WHERE email=?",(useremail,))
    username=cursor.fetchone()
    print(username)
    cursor.execute("SELECT wallet FROM user WHERE email=?", (useremail,))
    wallet_money=cursor.fetchone()
    # Close the connection
    conn.close()
    name=navbar_name[1]
    
    
    
    
    # Render the dashboard template with the username and message
    return render_template('dashboard.html', username=username[0],user=username[0][0].upper(), fav_icon=fav_icon, load_img=load_img,ip=ip,name=name,wallet=wallet_money[0])

@app.route('/payment',methods=['GET', 'POST'])
def payment():
    if 'username' in session:
        logout=1
        email=session['username']
        connection = connect_db()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM user WHERE email=?", (email,))
        user = cursor.fetchone()
        user=user[1][0]
        cursor.execute("SELECT wallet FROM user WHERE email=?", (email,))
        wallet_money=cursor.fetchone()
    else:
        wallet_money=[0]
        logout=0
        user="-1"
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        color = request.form.get('color')
        print(color)
        side = request.form.get('side')
        print(side)
        quantity = request.form.get('quantity')
        print(quantity)
    if color == '0':
        col="Black & White"
        col_cost=2
    else:
        print(color)
        col="Colour"
        col_cost=10
    if side == '0':
        sid = "Front and Back"
        sid_cost=0.8
    else:
        print(side)
        sid = "Single Side"
        sid_cost=1
    total=page*col_cost*sid_cost*int(quantity)

    # Create a unique identifier
    unique_id = str(uuid.uuid4())

    # Create the data to be encoded in the QR code, including the unique identifier
    # Create the QR code instance
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    data=ip+"/scan/" + unique_id
    # Add the data to the QR code
    qr.add_data(data)
    qr.make(fit=True)

    # Create an image from the QR code instance
    img = qr.make_image(fill_color="black", back_color="white")

    # Save the image
    img.save("static/images/qr.png")   
    # Add the identifier to the qr_codes dictionary
    qr_codes[unique_id] = True

    

    return render_template('payment.html', fav_icon=fav_icon, load_img=load_img, order_no=order_no, tod_date=tod_date,pages=page,
                           color=col,side=sid,quantity=quantity,total=total,sid_cost=sid_cost,col_cost=col_cost,qr_code_id=unique_id, data=data,qr_img=qr_img,user=user,ip=ip,wallet=wallet_money[0])

@app.route("/scan/<qr_code_id>")
def scan_qr_code(qr_code_id):
    # Check if the scanned QR code's identifier exists in the qr_codes dictionary
    if qr_codes.get(qr_code_id):
        # remove the scanned qr code from the dictionary
        qr_codes.pop(qr_code_id)
        data=ip+"/completed.html"
        return "Payment Completed"#render_template("completed.html", url=data)
    else:
        return "Already Scanned!"#render_template("scanned.html")

# contact page has been added-Meena
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if 'username' in session:
        logout=1
        email=session['username']
        connection = connect_db()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM user WHERE email=?", (email,))
        user = cursor.fetchone()
        user=user[1][0]
        name=navbar_name[1]
        cursor.execute("SELECT wallet FROM user WHERE email=?", (email,))
        wallet_money=cursor.fetchone()
        
        #print(wallet_money)
    else:
        wallet_money=[0]
        logout=0
        user="-1"
        name=navbar_name[0]    #return redirect(url_for('dashboard'))
    return render_template('contact.html', fav_icon=fav_icon, load_img=load_img,logout=logout,user=user.upper(),ip=ip,name=name,wallet=wallet_money[0])


@app.route('/team', methods=['GET', 'POST'])
def team():
    if 'username' in session:
        logout=1
        email=session['username']
        connection = connect_db()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM user WHERE email=?", (email,))
        user = cursor.fetchone()
        user=user[1][0]
        name=navbar_name[1]
        cursor.execute("SELECT wallet FROM user WHERE email=?", (email,))
        wallet_money=cursor.fetchone()
    else:
        wallet_money=[0]
        logout=0
        user="-1"        
        name=navbar_name[0] 
        #return redirect(url_for('dashboard'))
    return render_template('team.html', fav_icon=fav_icon, load_img=load_img, sam=sam, sandy=sandy, vejay=vejay, meena=meena,logout=logout,user=user.upper(),ip=ip,name=name,wallet=wallet_money[0])



@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')


counter=0
otp=-1

@app.route('/verification', methods=['POST', 'GET'])
def verify():
    global counter
    global otp
    if 'username' in session:
        logout=1
        email=session['username']
        connection = connect_db()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM user WHERE email=?", (email,))
        user = cursor.fetchone()
        useremail = user[3]
        print(useremail)
        user=user[1][0]
        cursor.execute("SELECT wallet FROM user WHERE email=?", (email,))
        wallet_money=cursor.fetchone()
        if counter==0:
            try:
                otp = OTP() + " is your OTP"
                msg = MIMEMultipart()
                msg['From'] = 'PrintEase Verification'
                msg['To'] = useremail
                msg['Subject'] = 'PrintEase OTP Verification'
                msg.attach(MIMEText(otp, 'plain'))
                s = smtplib.SMTP('smtp.gmail.com', 587)
                s.starttls()
                s.login("201501503@rajalakshmi.edu.in", "#")
                s.sendmail(msg['From'], msg['To'], msg.as_string())
            except:
                return "<h1><a href='/dashboard'>Try Agin Later</a></h1>"
        counter+=1
    else:
        wallet_money=[0]
        logout=0
        user="-1"
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        ver=request.form['logpass']
        print(ver,otp)
        ver= ver+" is your OTP"
        if ver==otp:
            return redirect('/dashboard')
        else:
            return "Try Again"
    return render_template('verification.html',fav_icon=fav_icon, load_img=load_img,user=user,wallet=wallet_money[0])


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0")
