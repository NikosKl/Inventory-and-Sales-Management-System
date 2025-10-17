import sqlite3

connection = sqlite3.connect('inventory.sqlite')
cur = connection.cursor()

cur.execute('DROP TABLE IF EXISTS Products')
cur.execute('DROP TABLE IF EXISTS Sales')

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
        contact TEXT);''')

cur.execute('INSERT OR IGNORE INTO Products (name, category, price, stock_qty) VALUES ("Wireless Mouse - HyperSpeed", "Electronics", 24.99, 150)')
cur.execute('INSERT OR IGNORE INTO Products (name, category, price, stock_qty) VALUES ("Mechanical Keyboard V3 - Wireless", "Electronics", 89.99, 75)')
cur.execute('INSERT OR IGNORE INTO Products (name, category, price, stock_qty) VALUES ("Office Chair With Reclining", "Furniture", 129.99, 40)')
cur.execute('INSERT OR IGNORE INTO Products (name, category, price, stock_qty) VALUES ("Thermo Bottle - Navy Blue", "Accessories", 14.50, 200)')
cur.execute('INSERT OR IGNORE INTO Products (name, category, price, stock_qty) VALUES ("Notebook (A5) - Red", "Office", 4.25, 300)')

cur.execute('SELECT * FROM Products')

print('The available products are:\n')
for row in cur.fetchall():
    print(f'ID: {row[0]} | Name: {row[1]} | Category: {row[2]} | Retail Price: {row[3]} | Quantity: {row[4]}')

connection.commit()
cur.close()