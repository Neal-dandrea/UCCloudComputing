from flask import Flask, render_template, request, redirect, url_for, send_file, g
import sqlite3
import os
import csv

app = Flask(__name__)
UPLOAD_FOLDER = '/home/ubuntu/flaskapp/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
DATABASE = '/home/ubuntu/flaskapp/natlpark.db'
USERS_DATABASE = '/home/ubuntu/flaskapp/users.db'
app.config.from_object(__name__)

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ===========================
# DATABASE HELPER FUNCTIONS
# ===========================
def connect_to_database():
    return sqlite3.connect(app.config['DATABASE'])

def connect_users_db():
    return sqlite3.connect(USERS_DATABASE)

def get_db():
    db = getattr(g, 'db', None)
    if db is None:
        db = g.db = connect_to_database()
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

def execute_query(query, args=()):
    cur = get_db().execute(query, args)
    rows = cur.fetchall()
    cur.close()
    return rows

# ===========================
# REGISTRATION ROUTES
# ===========================
@app.route('/')
def home():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    email = request.form['email']
    address = request.form['address']

    word_count = None
    if 'file' in request.files:
        file = request.files['file']
        if file.filename:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            with open(filepath, 'r') as f:
                words = f.read().split()
                word_count = len(words)

    with connect_users_db() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO users (username, password, firstname, lastname, email, address)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (username, password, firstname, lastname, email, address))
        conn.commit()

    user_data = (0, username, password, firstname, lastname, email, address)
    return render_template('profile.html', user=user_data, word_count=word_count)

# ===========================
# LOGIN ROUTE
# ===========================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with connect_users_db() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
            user = cur.fetchone()
        if user:
            return render_template('profile.html', user=user)
        else:
            return "Login failed. User not found."
    return render_template('login.html')

# ===========================
# DOWNLOAD ROUTE
# ===========================
@app.route('/download')
def download():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    if files:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], files[0])
        return send_file(filepath, as_attachment=True)
    else:
        return "No uploaded files available."

# ===========================
# RUN FLASK APPLICATION
# ===========================
if __name__ == '__main__':
    app.run(debug=True)
