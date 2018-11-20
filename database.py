import sqlite3


conn = sqlite3.connect('mobileshopping.db')

def brand_table():
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS BRAND
              (
              name varchar(10) PRIMARY KEY,
              website varchar(100),
              logo varchar(100)
              ); ''')
    c.execute('''insert into brand values('Mi', 'https://www.mi.com/in/', '/static/mi-logo.png');''')
    c.execute('''insert into brand values('Samsung' , 'https://www.samsung.com/in/mobile/' , '/static/samsung.png' );''')
    c.execute('''insert into brand values('Apple' , 'https://www.apple.com/in/iphone/' , '/static/apple.png' );''')
    c.execute('''insert into brand values('Motorola' , 'https://www.motorola.in' , '/static/motorola.png'  );''')
    c.execute('''insert into brand values('Lenovo' , 'https://www.lenovo.com/in/en/smartphones/c/smartphones' , '/static/lenovo.png' );''')
    conn.commit()
    c.close()


def mobile_table():
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS MOBILE
    (
    model varchar(50) PRIMARY KEY,
    brand varchar(10) ,
    ram varchar(5),
    rom varchar(5),
    battery varchar(10),
    camera varchar(6),
    cost integer,
    constraint fkm foreign key(brand) references brand(name)
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
    CUST_ID INTEGER NOT NULL,
    MODEL varchar(50) NOT NULL,
    ORD_DATE VARCHAR(10),
    DEL_BOY_ID INTEGER,
    COST INTEGER,
    
    ); ''')


    
    
def del_details():
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS DELIVERY
        (
        ORD_DATE    VARCHAR(10)  ,
        DELI_DATE    VARCHAR(10)
        ); ''')


#mobile_table()
#dash()
order_table()

del_details()




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