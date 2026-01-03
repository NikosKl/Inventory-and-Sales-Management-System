import sqlite3

connection = sqlite3.connect('inventory.sqlite')
cur = connection.cursor()

cur.execute('PRAGMA FOREIGN_KEYS = 1;')

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
        supplier_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        UNIQUE (supplier_id, product_id)
        FOREIGN KEY (supplier_id) REFERENCES Suppliers(id) ON DELETE CASCADE,
        FOREIGN KEY (product_id) REFERENCES Products(id) ON DELETE CASCADE);''')

connection.commit()
cur.close()