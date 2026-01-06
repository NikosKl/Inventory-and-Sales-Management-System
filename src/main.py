import pandas as pd
from src.menu_manager import product_menu, sales_menu, supplier_menu, reports_menu
from src.helpers import get_valid_input
from data.db import get_connection

connection = get_connection()
cur = connection.cursor()

while True:
    print('\n--- Inventory Management System ---')
    print(
        '\n1) Products'
        '\n2) Sales'
        '\n3) Suppliers'
        '\n4) Report & Analytics'
        '\n5) Exit')
    user_input = get_valid_input('\nEnter Choice: ',['1','2','3','4','5'])
    if user_input == '1':
        product_menu(cur)
    elif user_input == '2':
        sales_menu(cur, pd)
    elif user_input == '3':
        supplier_menu(cur, pd)
    elif user_input == '4':
        reports_menu(cur, pd)
    else:
        exit_confirmation = get_valid_input('\nAre you sure you want to exit? (y/n): ',['y','n'])
        if exit_confirmation == 'y':
            connection.commit()
            cur.close()
            break 
        else:
            pass