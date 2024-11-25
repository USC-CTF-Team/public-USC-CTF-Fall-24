from pathlib import Path
from flask import Flask, render_template, request, redirect, session, g, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from waitress import serve

import sqlite3
from uuid import uuid4
from datetime import datetime, timedelta
import os

from multisetup import setup

app = Flask(__name__)
app.secret_key = '$SuperS3cr3tK3Y!!!!'

# Database IDs, one for each competitor 
id_creation_time = dict()  # ID -> datetime that the db was created
def id_exists(id):
    return id in id_creation_time.keys()

def clear_db_files():
    for f in os.listdir(os.getcwd()):
        if f.endswith(".db"):
            db_path = os.path.join(os.getcwd(), f)
            print(f"Deleting {db_path}")
            os.remove(db_path)


@app.route('/', methods=['GET'])
def index():
    ids_for_deletion = []
    # Clean up old dbs
    for db_id, creation_dt in id_creation_time.items():
        if datetime.now() - creation_dt > timedelta(minutes=10):
            ids_for_deletion.append(db_id)

    for db_id in ids_for_deletion:
        try: 
            db_path = str(db_id) + '.db'
            print(f"Deleting {db_path}")
            Path.unlink(db_path, missing_ok=True)
            id_creation_time.pop(db_id)
        except Exception as e:
            print(f"Could not delete {db_path}")
            print(e)

    # Create new database for this user
    new_id = uuid4()
    while id_exists(new_id):
        new_id = uuid4()
    id_creation_time[new_id] = datetime.now()
    print(f"Current db_id dictionary: {id_creation_time}")
    print(f"Creating {new_id}.db at {str(id_creation_time[new_id])}; requested by {request.remote_addr}")
    setup(new_id)
    return redirect(f'/{new_id}/dashboard')

def get_db(db_id):
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(str(db_id) + ".db")
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/expired', methods=['GET'])
def expired():
    return '''Your instance expired. <a href="/">Create a new instance</a>'''

@app.route('/<uuid:db_id>/register', methods=['GET', 'POST'])
def register(db_id):
    if not id_exists(db_id):
        return redirect(url_for('expired'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = get_db(db_id).cursor()
        try:
            cursor.execute(f"INSERT INTO users (username, password) VALUES ('{username}', '{generate_password_hash(password)}')")
            get_db(db_id).commit()
            return redirect(f'/{db_id}/login')
        except sqlite3.IntegrityError:
            return "Username already taken."
        except sqlite3.OperationalError:
            print(f"Syntax error when registering from {request.remote_addr}")
            return "Error when registering"

    return render_template('register.html', db_id=db_id)

@app.route('/<uuid:db_id>/login', methods=['GET', 'POST'])
def login(db_id):
    if not id_exists(db_id):
        return redirect(url_for('expired'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = get_db(db_id).cursor()

        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()

        if user and check_password_hash(user['password'], password):
            session['username'] = user['username']
            return redirect(f'/{db_id}/dashboard')
        else:
            return "Invalid credentials."

    return render_template('login.html', db_id=db_id)

@app.route('/<uuid:db_id>/dashboard')
def dashboard(db_id):
    if not id_exists(db_id):
        return redirect(url_for('expired'))
    
    if 'username' not in session:
        return redirect(f'/{db_id}/login')

    username = session['username']
    cursor = get_db(db_id).cursor()

    if username == 'admin':
        cursor.execute("SELECT flag FROM flags")
        flag = cursor.fetchone()['flag']
        return render_template('dashboard.html', username=username, flag=flag, db_id=db_id)

    return render_template('dashboard.html', username=username, flag=None, db_id=db_id)

if __name__ == '__main__':
    clear_db_files()
    serve(app, host='0.0.0.0', port=5000, threads=6)
