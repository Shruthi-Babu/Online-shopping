from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, SelectField, IntegerField
from passlib.hash import sha256_crypt
import sqlite3
from functools import wraps
import timeit
import datetime
import logging, os
from werkzeug.utils import secure_filename


#from flask_uploads import UploadSet, configure_uploads, IMAGES
UPLOAD_FOLDER = '/static'
ALLOWED_EXTENSIONS = set([ 'png', 'jpg', 'jpeg', 'gif'])



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
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


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
    locality = SelectField('Locality', choices=[('Jayanagar', 'Jayanagar'), ('TR Nagar', 'TR Nagar'), ('Malleshwaram', 'Malleshwaram'), ('Girinagar', 'Girinagar'), ('Vijaynagar', 'Vijaynagar'), ('Other', 'Other')])


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

        c = conn.cursor()
        c.execute("INSERT INTO CUSTOMER(name, email,phone, password, door_num, street, locality) VALUES(?,?,?,?,?,?,?)",
                    (name, email,phone, password, doornum, street, locality))
        conn.commit()
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


@app.route('/dashboard/<brand>', methods=['GET', 'POST'])
@is_logged_in
def chosen_brand(brand):
    conn = sqlite3.connect('mobileshopping.db')
    c = conn.cursor()
    c.execute("""SELECT * FROM mobile WHERE brand=?; """, (brand,))
    products = c.fetchall()
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

    now = datetime.date.today()
    week = datetime.timedelta(days=7)
    delivery_date = now + week

    c.execute('''select cost from mobile where model=?;''', (model,))
    data= c.fetchone()
    cost = data[0]

    c.execute('''select * from customer where email=?;''', (customer_email,))
    data= c.fetchone()
    custid= data[0]
    locality= data[7]
    c.execute('''select id from deliveryboy where locality=?;''', (locality,))
    boy=c.fetchone()
    boyid=boy[0]

    c.execute('''insert into orders(cust_id, model, ord_date, cost, del_boy_id) values (?,?,?,?, ?);''',(custid, model, now, cost, boyid))

    c.execute('''select * from delivery_dates where ord_date= ?;''', (now,))
    ord=c.fetchone()

    if not ord:
        c.execute('''insert into delivery_dates(ord_date, deli_date) values (?, ?);''', (now, delivery_date))
    conn.commit()

    c.execute('''select * from orders order by order_id desc ;''')
    result= c.fetchone()
    cost= round(result[5])
    model= result[2]

    c.execute('''select * from DELIVERYBOY where locality=?;''', (locality,))
    deldata= c.fetchone()
    name= deldata[1]
    flash('You have succesfully placed your order!', 'success')

    return render_template('order_details.html', model=model, cost=cost, cust_data=data, delivery_date=delivery_date, del_boy=deldata )

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



#-----------------------Admin----------------------


def is_admin_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'admin_logged_in' in session:
            return f(*args, *kwargs)
        else:
            return redirect(url_for('admin_login'))

    return wrap

@app.route('/login-admin', methods=['GET', 'POST'])
#@not_admin_logged_in
def admin_login():
    if request.method == 'POST':
        # GEt user form
        email = request.form['email']
        password_candidate = request.form['password']

        conn = sqlite3.connect('mobileshopping.db')
        c = conn.cursor()

        # Get user by username
        c.execute("SELECT * FROM admin WHERE email = ?", [email])
        if c is None:
            flash('Incorrect login', 'danger')
            return render_template('admin-login.html')

        #if c is not None:
        else:
            data = c.fetchone()
            id=data[0]
            password = data[3]
            name = data[1]
            email = data[2]

        if password==password_candidate:
            session['admin_logged_in'] = True
            session['admin_id'] = id
            session['admin_name'] = name
            return redirect(url_for('admin'))

        else:
            flash('Incorrect login', 'danger')
            return render_template('admin-login.html')

    return render_template('admin-login.html')



@app.route('/admin-logout')
def admin_logout():
    #if 'admin_logged_in' in session:
     session.clear()
     flash('You are now logged out!', 'success')
     return redirect(url_for('home'))
    #return redirect(url_for('admin'))

@app.route('/admin')
@is_admin_logged_in
def admin():
    name = session['admin_name']


    return render_template('admin-page.html', name= name)


class AddMob(Form):
    model = StringField('Model', [validators.DataRequired('Please enter model'), validators.Length(min=1, max=50)])
    brand = StringField('Brand',[ validators.DataRequired('Please enter brand'), validators.Length(min=1, max=50)])
    ram = SelectField('RAM', choices=[('2GB', '2GB'), ('4GB', '4GB'), ('8GB', '8GB'), ('16GB', '16GB')])
    rom = SelectField('ROM', choices=[('2GB', '2GB'), ('4GB', '4GB'), ('8GB', '8GB'), ('16GB', '16GB'), ('32GB', '32GB'), ('64GB', '64GB'), ('128GB', '128GB'), ('256GB', '256GB')])
    battery = StringField('Battery', [validators.DataRequired('Please enter battery capacity'), validators.Length(min=1, max=50)])
    camera = StringField('Camera', [validators.DataRequired('Please enter camera capacity'), validators.Length(min=1, max=50)])
    cost= IntegerField('Cost', [validators.DataRequired('Please enter cost'), validators.Length(min=1, max=50)])



@app.route('/admin/add-mobile')
@is_admin_logged_in
def admin_add_mobile():
    name = session['admin_name']
    conn = sqlite3.connect('mobileshopping.db')
    form = AddMob(request.form)
    if request.method == 'POST' and form.validate():
        model = form.model.data
        brand = form.brand.data
        ram = form.ram.data
        rom = form.rom.data
        battery = form.battery.data
        battery= battery+ "MaH"

        camera = form.camera.data
        camera=camera+ "MP"
        cost = form.cost.data

        img = request.files['image']
        #save_photo = photos.save(img, folder='static')

        #app.logger.info(app.config['static'])
        img_name = secure_filename(img.filename)
        saved_path = os.path.join(app.config['UPLOAD_FOLDER'], img_name)
        img.save(saved_path)

        #filename = secure_filename(file.filename)
        #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        c = conn.cursor()
        c.execute("INSERT INTO mobile"
                  "(model, brand, ram, rom, battery, camera, cost) VALUES(?,?,?,?,?,?,?)", (model, brand, ram, rom, battery, camera, cost))
        conn.commit()
    return render_template('add-mob.html', form=form)




@app.route('/admin/delete-mobile', methods=['GET', 'POST'])
@is_admin_logged_in
def admin_delete_mobile():
    name = session['admin_name']
    conn = sqlite3.connect('mobileshopping.db')
    c = conn.cursor()
    c.execute('''select * from mobile;''')
    mobs=c.fetchall()

    return render_template('delete-mob.html', mobiles=mobs)


@app.route('/admin/delete-mobile/<model>', methods=['GET', 'POST'])
@is_admin_logged_in
def admin_delete_model(model):
    name = session['admin_name']
    conn = sqlite3.connect('mobileshopping.db')
    c = conn.cursor()
    c.execute('''delete from mobile where model=?;''', (model,))
    conn.commit()
    flash('You have deleted the selected model from the dashboard!', 'danger')
    return render_template('mob-deleted.html')




@app.route('/admin/view_orders')
@is_admin_logged_in
def admin_view_orders():
    name = session['admin_name']
    conn = sqlite3.connect('mobileshopping.db')
    c = conn.cursor()
    c.execute('''select o.order_id, c.name, o.model, o.cost, d.name from orders o, customer c, deliveryboy d where o.cust_id=c.id and o.del_boy_id=d.id ;''')
    data=c.fetchall()

    return render_template('view-orders.html', orders=data)



#---------------Admin end---------------------------


if __name__ == "__main__":
    #createtable()
    app.secret_key="secret123"
    app.run(debug=True)


