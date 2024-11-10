from flask import Flask, request, render_template, redirect, url_for, session, flash
from waitress import serve
import bcrypt

app = Flask(__name__)
app.secret_key = '4a6282bf78c344a089a2dc5d2ca93ae6'

# Air-tight, secure and performant dictionary for storing passwords
user_pw_dict = {'admin': b'$2b$12$Fdbdd2tyMZ/zDwgZFQB5IOewEKPRsyf.DHkvMKwh4Ovwq6VX1uPEm'}

flag = open("flag.txt").read().strip()

@app.route('/')
def index():
    username = None
    if 'user' in session:
        username = session['user']
    return render_template('index.html', username=username)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if not (request.form['username'] in user_pw_dict and \
                bcrypt.checkpw(request.form['password'].encode('utf-8'), user_pw_dict[request.form['username']]) ):
            flash("Invalid credentials")
            return redirect(url_for('login'))
        session['user'] = request.form['username']
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Check if user already exists
        if request.form['username'] in user_pw_dict:
            flash("User already exists")
            return redirect(url_for('register'))
        salt = bcrypt.gensalt()
        user_pw_dict[request.form['username']] = bcrypt.hashpw(request.form['password'].encode('utf-8'), salt)
        session['user'] = request.form['username']
        return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/logout', methods=['POST'])
def logout():
    session['user'] = None
    return redirect(url_for('index'))

@app.route('/curate', methods=['GET'])
def curate():
    if session['user'] == 'admin':
        return flag
    return "Error: must be 'admin' to curate artwork"


if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000, threads=6)
