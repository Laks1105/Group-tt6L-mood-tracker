from flask import Flask, render_template, request, redirect, session, flash, url_for

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Simulated user database (you can later connect to a real database)
users = {
    "user@example.com": "password123"
}

@app.route('/')
def home():
    if 'user' in session:
        return f"Welcome, {session['user']}! <br><a href='/logout'>Logout</a>"
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['Email']
        password = request.form['password']
        if email in users and users[email] == password:
            session['user'] = email
            flash("Login successful!")
            return redirect(url_for('home'))
        flash("Invalid email or password.")
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("You have been logged out.")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
