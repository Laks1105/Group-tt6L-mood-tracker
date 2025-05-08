import sqlite3
from flask import Flask, render_template, request, redirect, session

# Create the Flask app
app = Flask(__name__)
app.secret_key = 'any_random_secret_key'  # Needed to keep users logged in

# This function sets up the database and table
def setup_database():
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            password TEXT
        )
    ''')
    connection.commit()
    connection.close()

# Login route - shows form and checks credentials
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get login info
        email = request.form['email']
        password = request.form['password']

        # Look up user in database
        connection = sqlite3.connect("users.db")
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM users WHERE email = ? AND password = ?", (email, password))
        user = cursor.fetchone()
        connection.close()

        if user:
            session['username'] = user[0]  # Save user name in session
            return redirect('/dashboard')
        else:
            return "Email or password is incorrect."
    return render_template('login.html')


# Run the app
if __name__ == '__main__':
    setup_database()  # Make sure database and table exist
    app.run(debug=True)
