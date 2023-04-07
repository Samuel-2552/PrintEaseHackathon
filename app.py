from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/CustLog')
def CustLog():
    return render_template('CustLog.html')

@app.route('/buslog')
def buslog():
    return render_template('buslog.html')

if __name__ == '__main__':
    app.run(debug=True)