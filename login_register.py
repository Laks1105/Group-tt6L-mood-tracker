from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'your_super_secret_key_here'

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

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['Email']
        password = request.form['password']

        # Authenticate user
        with sqlite3.connect('user_id_password.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
            user = cursor.fetchone()

        if user:
            session['username'] = user[1] 
            return redirect(url_for('mood_selector'))
        else:
            return "Invalid username or password. Please try again."

    return render_template('login.html')


# Register page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm-password']

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

#Mood Selecting option - User's selecting their mood
@app.route('/mood', methods=['GET', 'POST'])
def mood_selector():
    name = session.get('username', 'Guest')
    mood_options = [("Happy", "😊"), ("Sad", "😔"), ("Angry", "😡"),
                    ("Relax", "🍃"), ("Stress", "🌀"), ("Energetic", "⚡")]
    if request.method == 'POST':
        selected_mood = request.form.get('mood')
        return f"{name}, You chose {selected_mood} Today"
    return render_template('Mood_selection.html', moods=mood_options)


# Run app
if __name__ == '__main__':
    if not os.path.exists('user_id_password.db'):
        init_db()
    app.run(debug=True)


