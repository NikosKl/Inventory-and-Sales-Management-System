import sqlite3
from product_manager import get_valid_input, add_product, update_product, delete_product, show_all
from sales_manager import record_sale, show_sales
from supplier_manager import add_supplier, delete_supplier, update_supplier, show_all_suppliers

connection = sqlite3.connect('inventory.sqlite')
cur = connection.cursor()

while True:
    print('\n--- Inventory Management System ---')
    user_input = get_valid_input(
        '\nEnter (1) - Products'
        '\nEnter (2) - Sales'
        '\nEnter (3) - Suppliers'
        '\nEnter (4) - Save/Exit ',['1','2','3','4'])
    if user_input == '1':
        print('\n--- Product Menu ---')
        products_menu = get_valid_input(
            '\nEnter (1) - Add a product'
            '\nEnter (2) - Update a product'
            '\nEnter (3) - Delete a product'
            '\nEnter (4) - Show product list ',['1','2','3','4'])
        if products_menu == '1':
            add_product(cur)
        elif products_menu == '2':
            update_product(cur)
        elif products_menu == '3':
            delete_product(cur)
        else:
            show_all(cur)
    elif user_input == '2':
        print('\n--- Sales Menu ---')
        sales_menu = get_valid_input(
            '\nEnter (1) - Record a sale'
            '\nEnter (2) - Show Sales ',['1','2'])
        if sales_menu == '1':
            record_sale(cur)
        else:
            show_sales(cur)
    elif user_input == '3':
        print('\n--- Supplier Menu ---')
        suppliers_menu = get_valid_input(
            '\nEnter (1) - Add a Supplier'
            '\nEnter (2) - Update a Supplier'
            '\nEnter (3) - Delete a Supplier'
            '\nEnter (4) - Show all Suppliers ',['1','2','3','4'])
        if suppliers_menu == '1':
            add_supplier(cur)
        elif suppliers_menu == '2':
            update_supplier(cur)
        elif suppliers_menu == '3':
            delete_supplier(cur)
        else:
            show_all_suppliers(cur)
    else:
        exit_confirmation = get_valid_input('\nAre you sure you want to exit? (y/n): ',['y','n'])
        if exit_confirmation == 'y':
            connection.commit()
            cur.close()
            break 
        else:
            continue