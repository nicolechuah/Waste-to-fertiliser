from flask import Flask, render_template, request, redirect, url_for



app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html', title = "Products")

@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/join-us')
def join_us():
    return render_template('join-us.html')


if __name__ == '__main__':
    app.run(debug=True)
