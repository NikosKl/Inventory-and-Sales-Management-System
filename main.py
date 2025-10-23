import sqlite3
import pandas as pd
from product_manager import get_valid_input, add_product, update_product, delete_product, show_all
from sales_manager import record_sale, show_sales
from supplier_manager import add_supplier, delete_supplier, update_supplier, show_all_suppliers, assign_products_to_supplier
from reports_manager import total_revenue, best_seller, total_orders, stock_report, low_stock_report, active_suppliers, supplier_product_coverage, products_without_supplier

connection = sqlite3.connect('inventory.sqlite')
cur = connection.cursor()

while True:
    print('\n--- Inventory Management System ---')
    user_input = get_valid_input(
        '\nEnter (1) - Products'
        '\nEnter (2) - Sales'
        '\nEnter (3) - Suppliers'
        '\nEnter (4) - Report & Analytics'
        '\nEnter (5) - Exit ',['1','2','3','4','5'])
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
            '\nEnter (4) - Assign products to Suppliers'
            '\nEnter (5) - Show all Suppliers ',['1','2','3','4', '5'])
        if suppliers_menu == '1':
            add_supplier(cur)
        elif suppliers_menu == '2':
            update_supplier(cur)
        elif suppliers_menu == '3':
            delete_supplier(cur)
        elif suppliers_menu == '4':
            assign_products_to_supplier(cur, pd)
        else:
            show_all_suppliers(cur)
    elif user_input == '4':
        print('\n--- Reports & Analytics Menu ---')
        reports_menu = get_valid_input(
            '\nEnter (1) - Sales Report'
            '\nEnter (2) - Inventory Report'
            '\nEnter (3) - Supplier Report ',['1','2','3'])
        if reports_menu == '1':
            print('\n--- Sales Reports Menu ---')
            sales_report_menu = get_valid_input(
                '\nEnter (1) - Total Sales Revenue'
                '\nEnter (2) - Best Seller products'
                '\nEnter (3) - Total Orders ',['1','2','3'])
            if sales_report_menu == '1':
                total_revenue(pd, connection)
            elif sales_report_menu == '2':
                best_seller(pd, connection)
            else:
                total_orders(cur)
        elif reports_menu == '2':
            print('\n--- Inventory Report Menu ---')
            inventory_reports_menu = get_valid_input(
                '\nEnter (1) - Inventory Stock Report'
                '\nEnter (2) - Low Stock Report ',['1','2'])
            if inventory_reports_menu == '1':
                stock_report(pd, connection)
            else:
                low_stock_report(pd, connection)
        elif reports_menu == '3':
            print('\n--- Supplier Report Menu ---')
            supplier_report_menu = get_valid_input(
                '\nEnter (1) - Supplier info'
                '\nEnter (2) - Products per Supplier'
                '\nEnter (3) - Show products without Supplier ',['1','2','3'])
            if supplier_report_menu == '1':
                active_suppliers(connection,pd)
            elif supplier_report_menu == '2':
                supplier_product_coverage(connection, pd)
            else:
                products_without_supplier(connection, pd)
    else:
        exit_confirmation = get_valid_input('\nAre you sure you want to exit? (y/n): ',['y','n'])
        if exit_confirmation == 'y':
            connection.commit()
            cur.close()
            break 
        else:
            pass