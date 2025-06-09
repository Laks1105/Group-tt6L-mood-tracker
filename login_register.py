from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,timedelta
import sqlite3
import random
import os

app = Flask(__name__, template_folder='templates')

import logging
from logging import StreamHandler

handler = StreamHandler()
handler.setLevel(logging.DEBUG)
app.logger.addHandler(handler)
app.logger.setLevel(logging.DEBUG)

# Set secret key for sessions
app.config['SECRET_KEY'] = 'your_super_secret_key_here'

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mood_tracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  

# Installing the database
db = SQLAlchemy(app)

# Your models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    mood_entries = db.relationship('MoodEntry', backref='user', lazy=True)

class MoodEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    mood = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Create the database and tables
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

# route for Home page to login page
@app.route('/')
def homepage():
    return redirect(url_for('login'))

# route for Login page
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

        #checking if username and password are correct 
        if user:
            session['username'] = user[1]  
            session['user_id'] = user[0]   
            return redirect(url_for('mood_selector'))
        else:
            return render_template('login.html', error="Incorrect Email or password. Try again!")

    return render_template('login.html')


# Route for Register page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            name = request.form['name'] #ask user for name
            email = request.form['email'] #ask user for email id
            password = request.form['password'] #ask user for password
            confirm = request.form['confirm-password'] # confirming the password

            if password != confirm:
                return render_template('register.html', error="Passwords do not match.")

            if not os.path.exists('user_id_password.db'):
                init_db()

            with sqlite3.connect('user_id_password.db') as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                    (name, email, password)
                )
                conn.commit()

            return redirect(url_for('login'))

        except Exception as e:
            # This will output the exact error in your Render logs:
            print("🛑 Registration Error:", repr(e))
            return f"Internal error during registration: {e}", 500

    return render_template('Register.html')



# View all users 
@app.route('/users')
def list_users():
    with sqlite3.connect('user_id_password.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, email FROM users")
        users = cursor.fetchall()
    return render_template('users.html', users=users)

# Route for Mood Selection (user selecting the mood)
@app.route('/mood', methods=['GET', 'POST'])
def mood_selector():
    name = session.get('username', 'Guest')  # Getting username 
    user_id = session.get('user_id')  # Getting user id

    if request.method == 'POST':
        selected_mood = request.form.get('mood')  # User selecting their mood
        
        # Saving the mood in database
        mood_entry = MoodEntry(user_id=user_id, mood=selected_mood)
        db.session.add(mood_entry)
        db.session.commit()

        # Options based on selected mood
        if selected_mood == 'Happy':
            return redirect(url_for('happy_mood_opt')) #if user choose happy
        elif selected_mood == 'Sad':
            return redirect(url_for('sad_mood_opt'))  #if user choose sad
        elif selected_mood == 'Stress':
            return redirect(url_for('stress_mood_opt')) #if user choose stress
        elif selected_mood == 'Angry':
            return redirect(url_for('angry_mood_opt'))
        elif selected_mood == 'Relax':
            return redirect(url_for('relax_mood_opt'))
        elif selected_mood == 'Energetic':
            return redirect(url_for('energetic_mood_opt'))
        #Options based on Selected mood

    return render_template('Mood_selection.html', username=name)

#Happy Mood Selection
@app.route('/mood/happy')
def happy_mood_opt():
    username = session.get('username', 'Guest')
    return render_template('Song_Selection_Happy_1.html', username=username)

#Sad Mood Selection
@app.route('/mood/sad')
def sad_mood_opt():
    username = session.get('username', 'Guest')
    return render_template('Song_Selection_Sad_1.html', username=username)

#Stress Mood Selection
@app.route('/mood/stress')
def stress_mood_opt():
    username = session.get('username', 'Guest')
    return render_template('Song_Selection_Stress_1.html', username=username)

#Angry Mood Selection
@app.route('/mood/angry')
def angry_mood_opt():
    username = session.get('username', 'Guest')
    return render_template('Song_Selection_Angry_1.html', username=username)

#Relaxed Mood Selection
@app.route('/mood/relax')
def relax_mood_opt():
    username = session.get('username', 'Guest')
    return render_template('Song_Selection_Relax_1.html', username=username)

#Energetic Mood Selection
@app.route('/mood/energetic')
def energetic_mood_opt():
    username = session.get('username', 'Guest')
    return render_template('Song_Selection_Energetic_1.html', username=username)

# Mood statistics route
@app.route('/graph')
def stats():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']  # Get logged-in user ID

    # Weekly range
    today = datetime.today()
    start_of_week = today - timedelta(days=today.weekday())  # Monday
    end_of_week = start_of_week + timedelta(days=7)

    moods = ['Happy', 'Sad', 'Energetic', 'Stress', 'Relax', 'Angry']

    mood_counts = [
        MoodEntry.query.filter(
            MoodEntry.user_id == user_id,
            MoodEntry.mood == mood,
            MoodEntry.timestamp >= start_of_week,
            MoodEntry.timestamp < end_of_week
        ).count()
        for mood in moods
    ]

    return render_template('statistic_page_1.html', mood_counts=mood_counts)


quotes = [
    "The future belongs to those who believe in the beauty of their dreams. -Eleanor Roosevelt",
    "I was smiling yesterday, I am smiling today and I will smile tomorrow. Simply because life is too short. -Santosh Kalwar",
    "Any fool can be happy. It takes a man with real heart to make beauty out of the stuff that makes us happy. -Clive Barker",
    "It always seems impossible until it’s done. – Nelson Mandela",
    "Be the reason someone smiles today. Be the reason someone feels loved and believes that goodness still exists in people. -C. JoyBell C.",
    "Your time is limited, so don't waste it living someone else's life. -Steve Jobs",
    "Do what you love, love what you do, and with all your heart give yourself to it. -Roy T. Bennett",
    "Even if you cannot change all the people around you, you can change the people you choose to be around you. -Roy T. Bennett",
    "Start where you are. Use what you have. Do what you can. -Arthur Asher",
    "The power of finding beauty in the humblest things makes home happy and life lovely. -Louisa May Alcott",
    "Each day brings new opportunities, allowing you to constantly live with love — be there for others — bringing light, kindness, and purpose into every moment. -G.K. Chesterton",
    "Life is funny. Things change, people change, but you will always be you, so stay true to yourself and embrace every twist and turn with grace and courage. -Zayn Malik",
    "Fear doesn't shut you down; it wakes you up. I've seen it. It's fascinating. -Veronica Roth",
    "Failure is simply the opportunity to begin again, this time more intelligently. -Henry Ford",
    "Success is not final, failure is not fatal: it is the courage to continue that counts. -Winston Churchill",
    "What lies behind us and what lies before us are tiny matters compared to what lies within us. – Ralph Waldo Emerson",
    "Believe in yourself and all that you are. Know that there is something inside you that is greater than any obstacle. -Christian D. Larson",
    "Success isn’t about how much money you make; it’s about the difference you make in people’s lives. -Michelle Obama",
    "The best way to predict the future is to create it. -Abraham Lincoln"
]


@app.route('/quotes')
def shuffling_quote_opt():
    return render_template('quotes_page_1.html')

@app.route('/shuffle')
def shuffle_quote():
    selected_quote = random.choice(quotes)
    return jsonify({'quote': selected_quote})

@app.route('/settings')
def settings():
    return render_template('settings_1.html')

#logout route 
@app.route('/logout')
def logout():
    session.clear()  # Clear all the data and login back
    return redirect(url_for('login')) 

@app.route('/check_templates')
def check_templates():
    path = os.path.join(app.root_path, 'templates', 'register.html')
    exists = os.path.exists(path)
    return f"register.html exists: {exists} at {path}"

if __name__ == '__main__':  
    if not os.path.exists('user_id_password.db'):
        init_db()

    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=True) 
