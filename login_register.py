from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Home page redirects to login
@app.route('/')
def home():
    return redirect(url_for('login'))

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['Email']
        password = request.form['password']
        # Just print input for now
        print("Login:", email, password)
        return "Logged in Successfully"
    return render_template('login.html')

# Register page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm-password']
        print("Register:", name, email, password, confirm)
        return "Registered "
    return render_template('register.html')

# Run the app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

