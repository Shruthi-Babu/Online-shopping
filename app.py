from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
#import Flask-MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
import sqlite3
from functools import wraps

# conn = sqlite3.connect('mobileshopping.db')

def createtable():
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS CUSTOMER
         (
         ID INTEGER PRIMARY KEY   AUTOINCREMENT  NOT NULL,
         NAME   VARCHAR(20)    NOT NULL,
         EMAIL  VARCHAR(20)    NOT NULL,
         PASSWORD   VARCHAR(20)    NOT NULL,
         DOOR_NUM    VARCHAR(10) ,
         STREET VARCHAR(20) ,
         LOCALITY   VARCHAR(20)  
         );''')


app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password',
    [validators.DataRequired(),  validators.EqualTo('confirm', message='Passwords do not match')])
    confirm = PasswordField('Confirm Password')

@app.route('/register', methods=['GET' , 'POST'])
def register():
    conn = sqlite3.connect('mobileshopping.db')
    form= RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        #username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        # Create cursor
        c = conn.cursor()

        # Execute query
        c.execute("INSERT INTO CUSTOMER(name, email,  password) VALUES(?,?,?)",
                    (name, email, password))
        # Commit to DB
        conn.commit()
        # Close connection
        c.close()

        flash('You are now registered and can log in', 'success')
        return redirect(url_for('index'))

    return render_template('register.html', form=form)

# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        name= request.form['name']
        email = request.form['email']
        password_candidate = request.form['password']

        # Create cursor
        conn = sqlite3.connect('mobileshopping.db')
        c = conn.cursor()

        # Get user by username
        result = c.execute("SELECT * FROM CUSTOMER WHERE email = ?", [email])

        #if result > 0:
        if c is not None:
            # Get stored hash
            data = c.fetchone()
            password = data[3] #3rd column in db
            name = data[1] #1st column in db

            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                # Passed
                session['logged_in'] = True
                session['name'] = name

                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
            # Close connection
            c.close()
        else:
            error = 'User not found'
            return render_template('login.html', error=error)

    return render_template('login.html')


# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('home'))


@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/contact")
def contact():
    return render_template('contact.html')

if __name__ == "__main__":
    #createtable()
    app.secret_key="secret123"
    app.run(debug=True)


