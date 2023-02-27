from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM user')
    users = cursor.fetchall()
    cursor.close()
    return render_template('index.html', users=users)

@app.route('/edit/<int:user_id>', methods=['GET', 'POST'])
def edit(user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM user WHERE id=?', (user_id,))
    user = cursor.fetchone()

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        wallet = request.form['wallet']
        EV = request.form['EV']
        cursor.execute('UPDATE user SET username=?, password=?, email=?, wallet=?, EV=? WHERE id=?', (username, password, email, wallet, EV, user_id))
        conn.commit()
        cursor.close()
        return redirect('/')
    
    cursor.close()
    return render_template('edit.html', user=user)

if __name__ == '__main__':
    app.run(debug=True)
