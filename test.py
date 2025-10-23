import pandas as pd
import sqlite3
from tabulate import tabulate
from product_manager import get_valid_input

def product_ids_input():
    while True:
        product_id = input("\nEnter product id's to assign (comma-separated): ")
        product_ids = [p_id.strip() for p_id in product_id.split(',') if p_id.strip().isdigit()]

        if not product_ids:
            print('\nNo valid product id entered.')
        else:
            product_ids = list(map(int, product_ids))
            print(f'\nThe selected ids are: {product_ids}')
            return product_ids

connection = sqlite3.connect('inventory.sqlite')
cur = connection.cursor()

supplier_data = pd.read_sql_query('SELECT name FROM Suppliers', connection)

print(f'\nThe active suppliers are: \n{tabulate(supplier_data, headers= 'keys', tablefmt='simple_grid')}')

valid_suppliers = supplier_data['name'].str.lower().tolist()

user_input = get_valid_input('\nSelect a supplier to assign products: ',valid_suppliers)

cur.execute('SELECT id from Suppliers WHERE LOWER(name) = ?', (user_input.lower(), ))
supplier_id = cur.fetchone()
if supplier_id is None:
    print('Supplier not Found')
else:
    supplier_id = supplier_id[0]

if user_input:
    data = pd.read_sql_query('SELECT * FROM Products', connection)
    print('\n' + tabulate(data, tablefmt='simple_grid', showindex=False))
    assigned_products = product_ids_input()

    for id in assigned_products:
        if id in data['id'].values:
            cur.execute('INSERT OR IGNORE INTO SupplierProducts (supplier_id, product_id) VALUES (?,?)',(supplier_id, id))
            print("\nID's have been updated!")
        else:
            print("\nProduct id doesn't exist")
    connection.commit()
else:
    exit()
