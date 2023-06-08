from flask import Flask, render_template, request, redirect, session
from flask_session import Session
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hds215sdf8sg54sdf8sd'
# app.config['SESSION_FILE_DIR'] = 'static\session_data.json'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

DB_NAME = 'database.db'

# Function to verify user login
def verify_login(email, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
    result = cursor.fetchone()

    conn.close()

    if result is not None:
        # Store user ID in the session
        session['user_id'] = result
        return True
    else:
        return False

    
# Function to verify business login
def verify_businesslogin(email, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM business WHERE email = ? AND password = ?", (email, password))
    result = cursor.fetchone()

    conn.close()

    if result is not None:
        # Store business ID in the session
        session['business_id'] = result[0]
        return True
    else:
        return False



@app.route('/')
def index():
    if 'user_id' in session:
        # User is authenticated, retrieve user details from the session
        user_id = session['user_id']

        # Retrieve user details from the database using the user_id
        # ...
        print(user_id)

        return render_template('index.html', user=user_id, log=1)
    else:
        # User is not authenticated, redirect to the login page
        return render_template('index.html')

@app.route('/about')
def about():
    if 'user_id' in session:
        # User is authenticated, retrieve user details from the session
        user_id = session['user_id']
        return render_template('about.html', user=user_id, log=1)
    else:
        # User is not authenticated, redirect to the about page
        return render_template('about.html')

@app.route('/services')
def services():
    if 'user_id' in session:
        # User is authenticated, retrieve user details from the session
        user_id = session['user_id']
        return render_template('services.html', user=user_id, log=1)
    else:
        # User is not authenticated, redirect to the services page
        return render_template('services.html')

@app.route('/servicedetails')
def servicedetails():
    if 'user_id' in session:
        # User is authenticated, retrieve user details from the session
        user_id = session['user_id']
        return render_template('service-details copy.html', user=user_id, log=1)
    else:
        # User is not authenticated, redirect to the service details page
        return render_template('service-details copy.html')
    # return render_template('service-details copy.html')


@app.route('/pricing')
def pricing():
    if 'user_id' in session:
        # User is authenticated, retrieve user details from the session
        user_id = session['user_id']
        return render_template('pricing.html', user=user_id, log=1)
    else:
        # User is not authenticated, redirect to the pricing page
        return render_template('pricing.html')
    # return render_template('pricing.html')

@app.route('/contact')
def contact():
    if 'user_id' in session:
        # User is authenticated, retrieve user details from the session
        user_id = session['user_id']
        return render_template('contact.html', user=user_id, log=1)
    else:
        # User is not authenticated, redirect to the contact page
        return render_template('contact.html')
    # return render_template('contact.html')

# Route for handling the login form
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Perform login verification
        if verify_login(email, password):
            # Redirect to the dashboard or desired page on successful login
            return redirect('/')
        # redirect('/dashboard')
        else:
            # Invalid credentials, render login page with an error message
            return render_template('login.html', error='Invalid email or password')
    if 'user_id' in session:
            # User is authenticated, retrieve user details from the session
        user_id = session['user_id']
        return redirect('/') 
    else:
        # Render the login page for GET requests
        return render_template('login.html')

@app.route('/loginbusiness', methods=['GET', 'POST'])
def loginbusiness():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Perform login verification
        if verify_businesslogin(email, password):
            # Redirect to the dashboard or desired page on successful login
            return "Logged In Successfully"
        # redirect('/dashboard')
        else:
            # Invalid credentials, render login page with an error message
            return render_template('login business.html', error='Invalid email or password')
    if 'user_id' in session:
        # User is authenticated, retrieve user details from the session
        user_id = session['user_id']
        return redirect('/')
    else:
        # User is not authenticated, redirect to the login business page
        return render_template('login business.html')
    # return render_template('login business.html')


# Route for handling the sign-up form
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']

        # Insert the user details into the 'users' table
        cursor.execute('''
            INSERT INTO users (first_name, last_name, email, password)
            VALUES (?, ?, ?, ?)
        ''', (first_name, last_name, email, password))
        conn.commit()

        conn.close()

        # Redirect to the login page or any desired page on successful signup
        return redirect('/login')
    
    if 'user_id' in session:
        # User is authenticated, retrieve user details from the session
        user_id = session['user_id']
        return redirect('/')
    else:
        # User is not authenticated, redirect to the register page
        return render_template('register.html')
    # Render the sign-up page for GET requests
    # return render_template('register.html')

@app.route('/registerbusiness', methods=['GET', 'POST'])
def registerbusiness():
    if request.method == 'POST':
        # Retrieve form data
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        business_name = request.form['business_name']
        business_address = request.form['business_address']
        business_phone = request.form['business_phone']

        # Create a connection to the SQLite database
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        # Execute the INSERT query to store the data in the 'business' table
        cursor.execute("INSERT INTO business (first_name, last_name, email, password, business_name, business_address, business_phone) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (first_name, last_name, email, password, business_name, business_address, business_phone))

        # Commit the changes and close the database connection
        conn.commit()
        conn.close()

        return redirect('/loginbusiness')
    if 'user_id' in session:
        # User is authenticated, retrieve user details from the session
        user_id = session['user_id']
        return redirect('/')
    else:
        # User is not authenticated, redirect to the register business page
        return render_template('register business.html')
    # return render_template('register business.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/forgot')
def forgot():
    if 'user_id' in session:
        # User is authenticated, retrieve user details from the session
        user_id = session['user_id']
        return redirect('/')
    else:
        # User is not authenticated, redirect to the forgot page
        return render_template('forgot-password.html')
    # return render_template('forgot-password.html')

@app.route('/forgotbusiness')
def forgotbusiness():
    if 'user_id' in session:
        # User is authenticated, retrieve user details from the session
        user_id = session['user_id']
        return redirect('/')
    else:
        # User is not authenticated, redirect to the forgot business page
        return render_template('forgot-password business.html')
    # return render_template('forgot-password business.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
