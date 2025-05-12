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


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
