from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# Initialize the database and create users table if it doesn't exist
def init_db():
    with sqlite3.connect('user_id_password.db') as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
    print("Database and users table created successfully.")

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
            return f"Welcome {user[1]}! You are logged in to our website."
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

@app.route('/', methods=['GET', 'POST'])
def mood_selector():
    if request.method == 'POST':
        selected_mood = request.form.get('mood')
        print(f"User selected mood: {selected_mood}")
        return redirect(url_for('You have selected a mood today', mood=selected_mood))
    
    return render_template('mood_selection.html')


# Run app
if __name__ == '__main__':
    if not os.path.exists('user_id_password.db'):
        init_db()
    app.run(debug=True)



