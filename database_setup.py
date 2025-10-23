import sqlite3

connection = sqlite3.connect('inventory.sqlite')
cur = connection.cursor()

cur.executescript('''
CREATE TABLE IF NOT EXISTS Products(
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        category TEXT,
        price REAL,
        stock_qty INTEGER);
CREATE TABLE IF NOT EXISTS Sales(
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER,
        quantity_sold INTEGER,
        sale_date DATETIME,
        FOREIGN KEY (product_id) REFERENCES Products(id));
CREATE TABLE IF NOT EXISTS Suppliers(
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        contact TEXT);
CREATE TABLE IF NOT EXISTS SupplierProducts(
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        supplier_id INTEGER,
        product_id INTEGER);''')

cur.execute('SELECT * FROM Products')

print('The available products are:\n')
for row in cur.fetchall():
    print(f'ID: {row[0]} | Name: {row[1]} | Category: {row[2]} | Retail Price: {row[3]} | Quantity: {row[4]}')

connection.commit()
cur.close()