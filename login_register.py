from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import sqlite3
import os

app = Flask(__name__)

# Set secret key for sessions
app.config['SECRET_KEY'] = 'your_super_secret_key_here'

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mood_tracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  

# Installing the database
db = SQLAlchemy(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    mood_entries = db.relationship('MoodEntry', backref='user', lazy=True)

# Mood Entry Model
class MoodEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    mood = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Create tables
with app.app_context():
    db.create_all()


def init_db():
    try:
        with sqlite3.connect('user_id_password.db') as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA integrity_check")
            result = cursor.fetchone()
            if result[0] != "ok":
                raise sqlite3.DatabaseError("Corrupt database")

            conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                )
            ''')
            print("Database and users table checked/created successfully.")
    except sqlite3.DatabaseError:
        os.remove('user_id_password.db')
        print("Corrupted DB found. Deleted and recreating.")
        init_db()

# Home page to login page
@app.route('/')
def homepage():
    return redirect(url_for('login'))

# Login page code
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['Email'] #inserting username
        password = request.form['password'] #inserting password

        # Authenticate user
        with sqlite3.connect('user_id_password.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
            user = cursor.fetchone()

        #checking username and password 
        if user:
            session['username'] = user[1]  
            session['user_id'] = user[0]   
            return redirect(url_for('mood_selector'))
        else:
            return "Invalid username or password. Please try again."

    return render_template('login.html')


# Register page code
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name'] #ask name
        email = request.form['email'] #ask email
        password = request.form['password'] #ask password
        confirm = request.form['confirm-password'] #confirm password

        if password != confirm:
            return "Passwords did not match! Try again"

        try:
            with sqlite3.connect('user_id_password.db') as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                               (name, email, password))
                conn.commit()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            return "Email already registered."

    return render_template('register.html')

# View all users 
@app.route('/users')
def list_users():
    with sqlite3.connect('user_id_password.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, email FROM users")
        users = cursor.fetchall()
    return render_template('users.html', users=users)

# Mood Selecting option - User's selecting their mood
@app.route('/mood', methods=['GET', 'POST'])
def mood_selector():
    name = session.get('username', 'Guest')  # Getting username 
    user_id = session.get('user_id')  # Getting user password

    if request.method == 'POST':
        selected_mood = request.form.get('mood')  # User selecting their mood
        # Saving the mood to the database
        mood_entry = MoodEntry(user_id=user_id, mood=selected_mood)
        db.session.add(mood_entry)
        db.session.commit()
        
        return f"{name}, you chose '{selected_mood}' Today!"
    if selected_mood == 'happy':
        return redirect(url_for('mood_happy')) #if user choose happy 
    
    return render_template('Mood_selection.html', username=name)

#Happy Mood
@app.route('/mood/happy')
def mood_happy():
    username = session.get('username', 'Guest')
    # Render a happy mood song selection page
    return render_template('Song_Selection_Happy_1.html', username=username)

if __name__ == '__main__':
    if not os.path.exists('user_id_password.db'):
        init_db()
    app.run(debug=True)