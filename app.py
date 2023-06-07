from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

DB_NAME = 'database.db'

# Function to verify user login
def verify_login(email, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Check if the email and password combination exists in the 'users' table
    cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
    result = cursor.fetchone()

    conn.close()

    # If a row is returned, the credentials are valid; otherwise, they are invalid
    if result is not None:
        return True
    else:
        return False


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

# Route for handling the login form
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Perform login verification
        if verify_login(email, password):
            # Redirect to the dashboard or desired page on successful login
            return "Logged In Successfully"
        # redirect('/dashboard')
        else:
            # Invalid credentials, render login page with an error message
            return render_template('login.html', error='Invalid email or password')

    # Render the login page for GET requests
    return render_template('login.html')

@app.route('/loginbusiness')
def loginbusiness():
    return render_template('login business.html')


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

    # Render the sign-up page for GET requests
    return render_template('register.html')

@app.route('/registerbusiness')
def registerbusiness():
    return render_template('register business.html')


@app.route('/forgot')
def forgot():
    return render_template('forgot-password.html')

@app.route('/forgotbusiness')
def forgotbusiness():
    return render_template('forgot-password business.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
