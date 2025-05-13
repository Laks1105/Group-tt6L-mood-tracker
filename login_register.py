from flask import Flask, render_template, request, redirect, url_for
import os

userdata_file ="user_database.db" # the file to store data

# Check if the file exists, if not create it 
def checkfile():
    if not os.path.exists(userdata_file):
        with open(userdata_file, "w") as file:
            file.write("email,password\n")  # Write a simple header

#to register new user only
def save_data(name,email,password,confirm=""):
    with open(userdata_file,"a") as file:#append mode 
        file.write(f"{name},{email},{password},{confirm}\n") #\n is to split it to next line


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
        return render_template('login.html')
    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True)


