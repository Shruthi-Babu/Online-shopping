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
    cost varchar(5),
    constraint fkm foreign key(brand) references brand(name)
    ); ''')
    c.execute('''insert into mobile values( 'Xiaomi Mi 4i' ,'Mi' , '2GB' , '16GB' ,'3120mAh', 	'13MP' ,'9900'); ''')
    c.execute('''insert into mobile values( 'Xiaomi Mi mix' ,'Mi' , '4GB' , '128GB' ,'4000mAh', 	'16MP' ,'34500'); ''')
    c.execute('''insert into mobile values( 'Xiaomi Mi 5' ,'Mi' , '3GB' , '32GB' ,'3000mAh', 	'16MP' ,'19990'); ''')
    c.execute('''insert into mobile values( 'Xiaomi Mi max' ,'Mi' , '3GB' , '32GB' ,'4850mAh', 	'16MP' ,'14999'); ''')
    c.execute('''insert into mobile values( 'Xiaomi Mi A1' ,'Mi' , '4GB' , '64GB' ,'3080mAh', 	'12MP' ,'14856'); ''')
    c.execute('''insert into mobile values( 'Xiaomi Mi 4i' ,'Mi' , '2GB' , '16GB' ,'3120mAh', 	'13MP' ,'9900'); ''')
    conn.commit()
    c.close()
    

def order_table():
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS ORDERS
    (
    ORDER_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    CUST_ID INTEGER NOT NULL,
    MODEL varchar(50) NOT NULL,
    ORD_DATE DATE,
    DELI_DATE DATE,
    DEL_BOY_ID INTEGER,
    COST VARCHAR(5)
    ); ''')
    
    
def dash():
    # Create cursor
    conn = sqlite3.connect('mobileshopping.db')
    c = conn.cursor()
    result = c.execute("SELECT * FROM BRAND")
    brands = c.fetchall()
    for brand in brands:
        print (brand)


#mobile_table()
#dash()
#order_table()