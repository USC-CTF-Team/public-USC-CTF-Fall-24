from flask import Flask, send_file, abort
from markupsafe import escape
from waitress import serve

app = Flask(__name__)
app.secret_key = 'aea4e4e0181801923bbcd877de40109'

@app.route('/')
def index():
    return path('index.html')

@app.route('/<path:filename>')
def path(filename):
    try:
        return send_file(escape(filename));
    except FileNotFoundError:
        abort(404)

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000, threads=6)
    #app.run(port=5000)
