from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/CustLog')
def CustLog():
    return render_template('CustLog.html')

@app.route('/BusLog')
def BusLog():
    return render_template('BusLog.html')
@app.route('/BusDash')
def BusDash():
    return render_template('BusDash.html')

if __name__ == '__main__':
    app.run(debug=True)