from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
#import Flask-MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, SelectField
from passlib.hash import sha256_crypt
import sqlite3
from functools import wraps
import timeit
import datetime

conn = sqlite3.connect('mobileshopping.db')

def createtable():
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS CUSTOMER
         (
         ID INTEGER PRIMARY KEY   AUTOINCREMENT  NOT NULL,
         NAME   VARCHAR(20)    NOT NULL,
         EMAIL  VARCHAR(20)    NOT NULL,
         PHONE INTEGER(10) NOT NULL,
         PASSWORD   VARCHAR(20)    NOT NULL,
         DOOR_NUM    VARCHAR(10) ,
         STREET VARCHAR(20) ,
         LOCALITY   VARCHAR(20)  
         );''')


app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home2.html')

class RegisterForm(Form):
    name = StringField('Name', [validators.DataRequired('Please enter name'), validators.Length(min=1, max=50)])
    email = StringField('Email',[ validators.DataRequired('Please enter email'), validators.Length(min=6, max=50)])
    phone = StringField('Phone', [validators.DataRequired('Please enter phone number'), validators.Length(min=10, max=10)])
    password = PasswordField('Password',
    [validators.DataRequired('Please enter password!'),  validators.EqualTo('confirm', message='Passwords do not match')])
    confirm = PasswordField('Confirm Password')

    doornum = StringField('Door No.', [validators.DataRequired('Please enter Door number'), validators.Length(min=1, max=50)])
    street = StringField('Street', [validators.DataRequired('Please enter Street'), validators.Length(min=1, max=50)])
    locality = SelectField('Locality', choices=[('Jayanagr', 'Jayanagar'), ('TR Nagar', 'TR Nagar'), ('Vijaynagar', 'Vijaynagar')])

#changeeeeeee it
@app.route("/register", methods=['GET' , 'POST'])
def register():
    conn = sqlite3.connect('mobileshopping.db')
    form= RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        phone = form.phone.data
        password = sha256_crypt.encrypt(str(form.password.data))

        doornum = form.doornum.data
        street = form.street.data
        locality = form.locality.data

        # Create cursor
        c = conn.cursor()
        c.execute("INSERT INTO CUSTOMER(name, email,phone, password, door_num, street, locality) VALUES(?,?,?,?,?,?,?)",
                    (name, email,phone, password, doornum, street, locality))
        # Commit to DB
        conn.commit()
        # Close connection
        c.close()

        flash('You are now registered and can log in', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
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
            password = data[4] #3rd column in db
            name = data[1] #1st column in db
            email= data[2]
            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                # Passed
                session['logged_in'] = True
                session['name'] = name
                session['email']= email

                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
            # Close connection
        else:
            error = 'User not found'
            return render_template('login.html', error=error)
        c.close()

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
@is_logged_in
def dashboard():
    # Create cursor
    conn = sqlite3.connect('mobileshopping.db')
    c = conn.cursor()
    c.execute("""SELECT * FROM BRAND;""")
    brands = c.fetchall()
    c.close()
    return render_template('dashboard.html', brands=brands)

@app.route('/dashboard/All', methods=['GET', 'POST'])
@is_logged_in
def view_all():
    conn = sqlite3.connect('mobileshopping.db')
    c = conn.cursor()
    c.execute("""SELECT * FROM mobile; """)
    products = c.fetchall()
    c.close()
    return render_template('mobile_models.html', products=products, brand= 'All')


#<h1 class="text-center" >{{mob_brand}}</h1>
#"{{ url_for('chosen_brand', brand=b[0] ) }}"
@app.route('/dashboard/<brand>', methods=['GET', 'POST'])
@is_logged_in
def chosen_brand(brand):
    conn = sqlite3.connect('mobileshopping.db')
    c = conn.cursor()
    c.execute("""SELECT * FROM mobile WHERE brand=?; """, (brand,))
    products = c.fetchall()
    # Close Connection
    c.close()
    return render_template('mobile_models.html', products=products, brand=brand)


@app.route('/dashboard-sorted-lh/<b>', methods=['GET', 'POST'])
@is_logged_in
def sort_lowtohigh(b):
    conn = sqlite3.connect('mobileshopping.db')
    c = conn.cursor()
    if b!='All':
        c.execute("""SELECT * FROM mobile WHERE brand=? ORDER BY cost ASC; """, (b,))
    else:
        c.execute("""SELECT * FROM mobile ORDER BY cost ASC; """)
    products = c.fetchall()
    c.close()
    return render_template('mobile_models.html', products=products, brand=b)

@app.route('/dashboard-sorted-hl/<b>', methods=['GET', 'POST'])
@is_logged_in
def sort_hightolow(b):
    conn = sqlite3.connect('mobileshopping.db')
    c = conn.cursor()
    if b!='All':
        c.execute("""SELECT * FROM mobile WHERE brand=? ORDER BY cost DESC; """, (b,))
    else:
        c.execute("""SELECT * FROM mobile ORDER BY cost DESC; """)
    products = c.fetchall()
    c.close()
    return render_template('mobile_models.html', products=products , brand=b)

# to add filter Not workingg
# class Filtering(Form):
#     ram = SelectField('RAM', choices=[('2GB', '2GB'), ('4GB', '4GB'), ('8GB', '8GB'), ('16GB', '16GB')])
#
# @app.route('/dashboard-sorted-hl/<b>', methods=['GET', 'POST'])
# def filter_ram(b):
#     conn = sqlite3.connect('mobileshopping.db')
#     form= Filtering(request.form)
#     if request.method == 'POST':
#         ram = form.ram.data
#         c=conn.cursor()
#         c.execute("""SELECT * FROM mobile WHERE brand=? AND ram=?; """, (b,ram))
#     products = c.fetchall()
#     c.close()
#     return render_template('mobile_models.html', products=products, brand=b)

# {% from "includes/_formhelpers.html" import render_field %}
#
#   <form method="POST" action="">
#       <div class="form-group">
#        {{render_field(form.ram, class_="form-control")}}
#       </div>
#   </form>





@app.route('/dashboard-order/<model>')
@is_logged_in
def place_order(model):
    conn = sqlite3.connect('mobileshopping.db')
    c = conn.cursor()
    custname = session['name']
    customer_email= session['email']

    #insert here
    now = datetime.date.today()
    week = datetime.timedelta(days=7)
    delivery_date = now + week

    c.execute(''' CREATE TRIGGER  IF NOT EXISTS del_date_details AFTER INSERT ON ORDERS
    BEGIN
       INSERT INTO DELIVERY( DELI_DATE) VALUES (?);
    END;''',(datetime.date.today(),  delivery_date))

    #now1 = datetime.datetime.now().date()

#    c.execute('create trigger if not exists calculate_sp after insert on stock
    # for each row begin
    #  update stock set sell_price = new.cost_price*1.18*1.2 where cycle_name = new.cycle_name;
    #  end')

    c.execute('''select cost from mobile where model=?;''', (model,))
    data= c.fetchone()
    cost = data[0]

    c.execute('''select * from customer where email=?;''', (customer_email,))
    data= c.fetchone()
    custid= data[0]

    c.execute('''insert into orders(cust_id, model, ord_date, cost) values (?,?,?,?);''',(custid, model,now, cost))
    c.execute('''insert into delivery(ord_date) values (?);''', (now,))
    conn.commit()

    flash('You have succesfully placed your order!', 'success')
    return render_template('order_details.html', model=model, cost=cost, cust_data=data, delivery_date='hi' )
    #return str(delivery_date)

#style="width: 50rem;"

#action="{{ url_for('shipping_details') }}"
def shipping_details():
    a=5
    print(a)


@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out!', 'success')
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


