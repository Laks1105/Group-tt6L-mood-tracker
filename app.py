from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flash messages

# Hardcoded user credentials (replace with database logic in real app)
USER_CREDENTIALS = {
    "test@example.com": "password123"
}

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('Email')
        password = request.form.get('password')

        # Authentication check
        if email in USER_CREDENTIALS and USER_CREDENTIALS[email] == password:
            return f"Welcome, {email}!"
        else:
            flash("Invalid email or password. Try again.")
            return render_template('login.html')

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
