import sqlite3


conn = sqlite3.connect('mobileshopping.db')

def brand_table():
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS BRAND
              (
              name varchar(10),
              website varchar(100),
              logo varchar(100),
              constraint pk_brand primary key(name)
              ); ''')

    c.execute('''insert into brand values('Mi', 'https://www.mi.com/in/', '/static/mi-logo.png');''')
    c.execute('''insert into brand values('Samsung' , 'https://www.samsung.com/in/mobile/' , '/static/samsung.png' );''')
    c.execute('''insert into brand values('Apple' , 'https://www.apple.com/in/iphone/' , '/static/apple.png' );''')
    #c.execute('''insert into brand values('Motorola' , 'https://www.motorola.in' , '/static/motorola.png'  );''')
    #c.execute('''insert into brand values('Lenovo' , 'https://www.lenovo.com/in/en/smartphones/c/smartphones' , '/static/lenovo.png' );''')
    conn.commit()
    c.close()


def mobile_table():
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS MOBILE
    (
    model varchar(50) ,
    brand varchar(10) ,
    ram varchar(5),
    rom varchar(5),
    battery varchar(10),
    camera varchar(6),
    cost integer,
    constraint pk_mob primary key(model),
    constraint fkm foreign key(brand) references brand(name) on delete cascade
    ); ''')

    c.execute('''insert into mobile values( 'Xiaomi Mi 4i' ,'Mi' , '2GB' , '16GB' ,'3120mAh', 	'13MP' ,9900); ''')
    c.execute('''insert into mobile values( 'Xiaomi Mi mix' ,'Mi' , '4GB' , '128GB' ,'4000mAh', 	'16MP' ,34500); ''')
    c.execute('''insert into mobile values( 'Xiaomi Mi 5' ,'Mi' , '3GB' , '32GB' ,'3000mAh', 	'16MP' ,19990); ''')
    c.execute('''insert into mobile values( 'Xiaomi Mi max' ,'Mi' , '3GB' , '32GB' ,'4850mAh', 	'16MP' ,14999); ''')
    c.execute('''insert into mobile values( 'Xiaomi Mi A1' ,'Mi' , '4GB' , '64GB' ,'3080mAh', 	'12MP' ,14856); ''')

    c.execute('''insert into mobile values( 'Samsung Galaxy A7' ,'Samsung' , '4GB' , '64GB' ,'3300mAh', '24MP' ,22945); ''')
    c.execute('''insert into mobile values( 'Samsung Galaxy J6' ,'Samsung' , '4GB' , '64GB' ,'3000mAh', 	'13MP' ,12900); ''')

    c.execute('''insert into mobile values( 'iPhone XS' ,'Apple' , '4GB' , '64GB' ,'3500mAh', '12MP' ,99900); ''')
    c.execute('''insert into mobile values( 'iPhone XS Max' ,'Apple' , '4GB' , '128GB' ,'4300mAh', '14MP' ,109900); ''')
    c.execute('''insert into mobile values( 'iPhone XR' ,'Apple' , '8GB' , '64GB' ,'3800mAh', '12MP' ,76900); ''')
    c.execute('''insert into mobile values( 'iPhone X' ,'Apple' , '16GB' , '256GB' ,'4000mAh', '24MP' ,144900); ''')

    conn.commit()
    c.close()
    

def order_table():
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS ORDERS
    (
    ORDER_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    CUST_ID number NOT NULL,
    MODEL varchar(50) NOT NULL,
    ORD_DATE VARCHAR(10),
    DEL_BOY_ID number,
    COST number,
    constraint fk_or1 foreign key(cust_id) references customer(id) on delete cascade,
    constraint fk_or2 foreign key(model) references mobile(model) on delete cascade,
    constraint fk_or3 foreign key(del_boy_id) references delivery_person(id) on delete set null    
    ); ''')


def delboy_tab():
    c = conn.cursor()

    c.execute('''create table if not exists DELIVERYBOY
    (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name varchar(20),
    phone number,
    locality varchar(20)
    );''')

    c.execute("insert into DELIVERYBOY (name, phone, locality)  values ('Amar', 8776544836, 'Jayanagar');")
    c.execute('''insert into DELIVERYBOY (name, phone, locality) values ('Akbar', 8777454836, 'Vijaynagar');''')
    c.execute('''insert into DELIVERYBOY (name, phone, locality) values ('Antony', 8274544836, 'TR Nagar');''')
    c.execute('''insert into DELIVERYBOY (name, phone, locality) values ('Harry', 877333836, 'Malleshwaram');''')
    c.execute('''insert into DELIVERYBOY (name, phone, locality) values ('John', 8783658836, 'Girinagar');''')
    c.execute('''insert into DELIVERYBOY (name, phone, locality) values ('Chris', 8783657836, 'Other');''')

    print("hi")

    
def del_details():
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS DELIVERY_DATES
        (
        ORD_DATE    VARCHAR(10)  ,
        DELI_DATE    VARCHAR(10)
        ); ''')


def trig():
    c= conn.cursor()
    c.execute(''' CREATE TRIGGER IF NOT EXISTS update_order_cost AFTER INSERT ON ORDERS
       FOR EACH ROW BEGIN
          UPDATE ORDERS SET cost= NEW.cost*1.12 where model=NEW.model;
       END;''')


def admin_details():
    c= conn.cursor()
    c.execute('''create table if not exists admin
    (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name varchar(20),
    email varchar(20),
    password varchar(20)
    );    ''')

    c.execute('''insert into admin (name, email, password) values ('Emma', 'emma@gmail.com', '12345');''')
    c.execute('''insert into admin (name, email, password) values ('Ginny', 'ginny@gmail.com', '11111');''')

    conn.commit()
    c.close()

#trig()

#brand_table()

#mobile_table()

#order_table()
#
# del_details()
#
#delboy_tab()
#admin_details()



#now = datetime.datetime.now().date()
    # now=datetime.date.today()
    # week = datetime.timedelta(days=7)
    # delivery_date = now + week
    #
    # c.execute(''' CREATE TRIGGER  IF NOT EXISTS del_date_details AFTER INSERT
    # ON ORDERS
    # BEGIN
    #    INSERT INTO DELIVERY(ORD_DATE, DELI_DATE) VALUES (?,?);
    # END;''',(datetime.datetime.now().date(),  delivery_date))