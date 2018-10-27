import sqlite3

conn = sqlite3.connect('mobileshopping.db')


def createtable():
    conn.execute('''CREATE TABLE IF NOT EXISTS CUSTOMER
         (
         ID INT PRIMARY KEY   AUTOINCREMENT  NOT NULL,
         NAME   VARCHAR(20)    NOT NULL,
         EMAIL  VARCHAR(20)    NOT NULL,
         PASSWORD   VARCHAR(20)    NOT NULL
         DOORNUM    VARCHAR(10),
         STREET VARCHAR(20),
         LOCALITY   VARCHAR(20);  
         );''')