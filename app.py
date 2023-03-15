from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
import os
import datetime
import PyPDF2
import qrcode
import time
import uuid
import math
import imghdr
from PIL import Image
from PIL import ImageOps
import hashlib
import random
import smtplib
import ssl

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


pay=0
ip="http://192.168.1.6:5000"
counter=0
file_counter=0
otp=-1
qr_codes={}
navbar_name=['GET STARTED','ORDER NOW']
today = datetime.date.today()
tod_date = today.strftime("%d-%m-%Y")
filepath=''
order_no=1
page=0
total=0
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

file_constant=""
useremailf=""
rv=0
ll=0

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

def notification():
    conn_cred = sqlite3.connect('cred.db')

    # Create a cursor
    cursor_cred = conn_cred.cursor()

    # Execute an SQL command to retrieve the first row from the user table
    cursor_cred.execute('SELECT * FROM user LIMIT 1')

    # Fetch the first row and print it
    row = cursor_cred.fetchone()
    email_from=row[1]
    decrypted=row[2]

    # Close the connection
    conn_cred.close()

    if 'username' in session:
        email=session['username']
        connection = connect_db()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM user WHERE email=?", (email,))
        user = cursor.fetchone()
        username = user[1]
        try:
            subject = f"PrintEase: Collect your document!"
            message = f"{username}, your document is printed and ready for the pickup.\nThank You for using PrintEase."
            # Create context
            simple_email_context = ssl.create_default_context()
            try:
                # Connect to the server
                print("Connecting to server...")
                TIE_server = smtplib.SMTP(smtp_server, smtp_port)
                TIE_server.starttls(context=simple_email_context)
                TIE_server.login(email_from, decrypted)
                print("Connected to server :-)")

                # Send the actual email
                print()
                print(f"Sending email to - {email}")
                TIE_server.sendmail(email_from, email, f"Subject: {subject}\n\n{message}")
                print(f"Email successfully sent to - {email}")

            # If there's an error, print it out
            except Exception as e:
                return e
        except Exception as e:
                return e
def verify():
    global otp
    import sqlite3

    # Connect to the database
    conn_cred = sqlite3.connect('cred.db')

    # Create a cursor
    cursor_cred = conn_cred.cursor()

    # Execute an SQL command to retrieve the first row from the user table
    cursor_cred.execute('SELECT * FROM user LIMIT 1')

    # Fetch the first row and print it
    row = cursor_cred.fetchone()
    email_from=row[1]
    decrypted=row[2]

    # Close the connection
    conn_cred.close()

    if 'username' in session:
        email=session['username']
        connection = connect_db()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM user WHERE email=?", (email,))
        user = cursor.fetchone()
        username = user[1]
        verify=user[5]
        if verify==0:
            try:
                otp = OTP() + " is your OTP"
                subject = f"Welcome to PrintEase {username}!"
                message = f"{otp}.\nPlease do not share it with anyone."
                # Create context
                simple_email_context = ssl.create_default_context()
                try:
                    # Connect to the server
                    print("Connecting to server...")
                    TIE_server = smtplib.SMTP(smtp_server, smtp_port)
                    TIE_server.starttls(context=simple_email_context)
                    TIE_server.login(email_from, decrypted)
                    print("Connected to server :-)")

                    # Send the actual email
                    print()
                    print(f"Sending email to - {email}")
                    TIE_server.sendmail(email_from, email, f"Subject: {subject}\n\n{message}")
                    print(f"Email successfully sent to - {email}")

                # If there's an error, print it out
                except Exception as e:
                    return e
            except Exception as e:
                return e


@app.route('/')
def landing():
    global pay
    if 'username' in session:
        logout=1
        email=session['username']
        connection = connect_db()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM user WHERE email=?", (email,))
        user = cursor.fetchone()
        print(user)
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
    if(pay==1):
        os.remove(file_constant)
    return render_template("landing.html", fav_icon=fav_icon, load_img=load_img,logout=logout,user=user.upper(),ip=ip,name=name,wallet=wallet_money[0],pay=pay)

@app.route('/aboutus')
def aboutus():
    #return redirect(url_for('dashboard'))
    return redirect("/#aboutus")   


# Signup function
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
        try:
            # Hash the password
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            cursor.execute("INSERT INTO user (username, password, email) VALUES (?, ?, ?)", (username, password_hash, email))
            connection.commit()
            connection.close()
        except:
            err_message="E-mail already registered!"
            return render_template('index.html',text="checked",message=err_message, fav_icon=fav_icon, load_img=load_img,ip=ip,no_load=0)
        return redirect('/login')
    return render_template('index.html', text="checked" ,fav_icon=fav_icon, load_img=load_img,ip=ip,no_load=1)

# Login function
@app.route('/login', methods=['GET', 'POST'])
def login():
    global order_no
    global ll
    if 'username' in session:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        try:
            useremail = request.form['logemail']
            password = request.form['logpass']
            connection = connect_db()
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM user WHERE email=?", (useremail,))
            user = cursor.fetchone()
            print(user)
        except:
            return "E-mail already Exists"
        if user:
            ll=1
            # Hash the entered password and compare with the stored hash
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            if password_hash == user[2]:
                session['username'] = useremail
                if useremail == 'printease2023@gmail.com':
                    return redirect('/admin')
                if user[5]==0:
                    return redirect('/verification')
                order_no+=1
                return redirect('/dashboard')
            else:
                err_message="Invalid mail or password!!"
                return render_template('index.html',mess=err_message, fav_icon=fav_icon, load_img=load_img,ip=ip,no_load=0)
        else:
            err_message="Invalid mail or password!!"
            return render_template('index.html',mess=err_message, fav_icon=fav_icon, load_img=load_img,ip=ip,no_load=0)
    return render_template('index.html', fav_icon=fav_icon, load_img=load_img,ip=ip,no_load=1)


@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    global rv
    if 'username' in session:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        useremailf = request.form['logemail']
        #print(useremail)
        connection = connect_db()
        cursor = connection.cursor()
        cursor.execute("SELECT email FROM user WHERE email=?", (useremailf,))
        user = cursor.fetchone()
        if user:
            rv=1
            global otp    

            # Connect to the database
            conn_cred = sqlite3.connect('cred.db')

            # Create a cursor
            cursor_cred = conn_cred.cursor()

            # Execute an SQL command to retrieve the first row from the user table
            cursor_cred.execute('SELECT * FROM user LIMIT 1')

            # Fetch the first row and print it
            row = cursor_cred.fetchone()
            email_from=row[1]
            decrypted=row[2]

            # Close the connection
            conn_cred.close()


            if(rv==1):        
                try:
                    otp = OTP() + " is your OTP"
                    subject = f"RESET YOUR PASSWORD!"
                    message = f"{otp}.\nUse this one time password for resetting your password.\n Please do not share it with anyone."
                    # Create context
                    simple_email_context = ssl.create_default_context()
                    try:
                        # Connect to the server
                        print("Connecting to server...")
                        TIE_server = smtplib.SMTP(smtp_server, smtp_port)
                        TIE_server.starttls(context=simple_email_context)
                        TIE_server.login(email_from, decrypted)
                        print("Connected to server :-)")

                        # Send the actual email
                        print()
                        print(f"Sending email to - {useremailf}")
                        TIE_server.sendmail(email_from, useremailf, f"Subject: {subject}\n\n{message}")
                        print(f"Email successfully sent to - {useremailf}")

                    # If there's an error, print it out
                    except Exception as e:
                        return e
                except Exception as e:
                    return e
            return redirect(url_for('forgotverification'))
        else:
                error="usernotfound"
                return render_template('forgot.html', fav_icon=fav_icon, load_img=load_img, ip=ip,error=error)
    return render_template('forgot.html', fav_icon=fav_icon, load_img=load_img, ip=ip)

@app.route('/forgotverification', methods=['GET', 'POST'])
def forgotverification():
    global useremailf
    print(useremailf)
    if 'username' in session:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        ver=request.form['logpass']
        print(ver,otp)
        ver= ver+" is your OTP"
        if ver==otp:
            return redirect('/resetpassword')
        else:
            return "<h1><a href='/dashboard'>Incorrect OTP!</a></h1>"
    return render_template('forgotverification.html', fav_icon=fav_icon, load_img=load_img, ip=ip)

@app.route('/resetpassword', methods=['GET', 'POST'])
def resetpassword():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        new=request.form['newpass']
        confirm=request.form['confirmpass']
        if new==confirm:
            try:
                
                connection = connect_db()
                cursor = connection.cursor()
                #newpass=hashlib.sha256(new.encode()).hexdigest()
                newpass=321
                cursor.execute("UPDATE user SET (otp=?) WHERE (email=?)", (newpass,useremailf,))
        
                connection.commit()
                connection.close()
                return redirect('/login')
            except:
                  return "Database error"
        else:
            matching_check="New password & confirm password doesn't match"
            check=True
            return render_template('resetpassword.html', fav_icon=fav_icon, load_img=load_img, ip=ip,checking=matching_check,flag=check)

    return render_template('resetpassword.html', fav_icon=fav_icon, load_img=load_img, ip=ip)


@app.route("/upload-file", methods=["POST"])
def upload_file():
    global filepath
    global page
    global file_counter
    file = request.files["file"]

    # Specify the directory name to create
    directory = "files/"+session['username']+'/'

    # Create the directory if it doesn't already exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    if file and file.content_type == "application/pdf":
        filename = directory+str(file_counter)+".pdf"
        file_counter+=1
        file.save(filename)
        print(filename) 
        pages=get_num_pages(filename)
        
        page=pages
        print("pages = ", page)
        return "File uploaded successfully!"
    if imghdr.what(file) is not None:
        filename = directory+str(file_counter)+".jpg"
        file.save(filename)
        file_counter+=1
        # Load the image
        image = Image.open(filename)

        # Convert the image to grayscale
        grayscale_image = image.convert('L')

        # Convert the inverted image to a color document
        color_document = ImageOps.colorize(grayscale_image, (0, 0, 0), (255, 255, 255))

        # Save the color document
        color_document.save(filename)
        print(filename)   
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
    print(wallet_money)
    conn.close()
    name=navbar_name[1]

    image_url=url_for('static', filename='image.jpg')
    
    
    
    
    # Render the dashboard template with the username and message
    return render_template('dashboard.html', username=username[0],user=username[0][0].upper(), fav_icon=fav_icon, load_img=load_img,ip=ip,name=name,wallet=wallet_money[0])

@app.route('/payment',methods=['GET', 'POST'])
def payment():
    global total
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
    global total,pay,file_constant
    if 'username' in session:
        email=session['username']
        connection = connect_db()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM user WHERE email=?", (email,))
        user = cursor.fetchone()
        user=user[1][0]
        cursor.execute("SELECT wallet FROM user WHERE email=?", (email,))
        wallet_money=cursor.fetchone()
    # Check if the scanned QR code's identifier exists in the qr_codes dictionary
    if qr_codes.get(qr_code_id):
        # remove the scanned qr code from the dictionary
        qr_codes.pop(qr_code_id)
        balance=wallet_money[0]-total
        print(balance)
        cursor.execute('UPDATE user SET wallet=? WHERE email=?', (balance, email))
        connection.commit()
        cursor.close()
        pay=1
        file_path = "files\\"+session['username']+"\\"
        file_name=os.listdir(file_path)
        file_name.sort()
        file_constant=file_path+file_name[len(file_name)-1]
        os.startfile(file_constant,"print")
        notification()
        time.sleep(5)
        return redirect('/')
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
    global pay
    pay=0
    session.pop('username', None)
    return redirect('/')

smtp_port = 587                 # Standard secure SMTP port
smtp_server = "smtp.gmail.com"  # Google SMTP Server


@app.route('/verification', methods=['POST', 'GET'])
def verification():
    global otp
    if 'username' in session:
        email=session['username']
        connection = connect_db()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM user WHERE email=?", (email,))
        user = cursor.fetchone()
        useremail = user[3]
        wallet_money=user[4]
        print(useremail)
        user=user[1][0]
    if request.method == 'POST':
        ver=request.form['logpass']
        print(ver,otp)
        ver= ver+" is your OTP"
        if ver==otp:
            EV=1
            wallet=wallet_money+20
            cursor.execute('UPDATE user SET EV=?, wallet=? WHERE email=?', (EV,wallet, email))
            connection.commit()
            cursor.close()
            return redirect('/dashboard')
        else:
            return "<h1><a href='/dashboard'>Try Again Later</a></h1>"
    return render_template('verification.html',fav_icon=fav_icon, load_img=load_img,user=user,wallet=wallet_money,ok=verify())


@app.route('/admin')
def index():
    try:
        if session['username'] == 'printease2023@gmail.com':
            
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM user')
            users = cursor.fetchall()
            cursor.close()
            return render_template('admin.html', users=users,fav_icon=fav_icon, load_img=load_img)
        else:
            return "Login as Admin"
    except:
        
            return "Login as Admin"
@app.route('/delete',methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        dbid=request.form['dbid']       
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('delete from user where id=?',(dbid))
        conn.commit()
        cursor.close()
        return redirect('/admin')
    else:
        return "User doesn't Exist"
       
        

@app.route('/edit/<int:user_id>', methods=['GET', 'POST'])
def edit(user_id):
    if session['username'] == 'printease2023@gmail.com':
        try:
        
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM user WHERE id=?', (user_id,))
            user = cursor.fetchone()
            if request.method == 'POST':
                username = request.form['username']
               
                email = request.form['email']
                wallet = request.form['wallet']
                EV = request.form['EV']
                cursor.execute('UPDATE user SET username=?,email=?, wallet=?, EV=? WHERE id=?', (username,email, wallet, EV, user_id))
                conn.commit()
                cursor.close()
                return redirect('/')
            
        except:
            return "Some error in Database"
        return render_template('edit.html', user=user,fav_icon=fav_icon, load_img=load_img)
    else:
        return "Login as admin"
    

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0")
