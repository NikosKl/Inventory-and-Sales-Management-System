import sqlite3
from product_manager import get_valid_input, add_product, update_product, delete_product, show_all

connection = sqlite3.connect('inventory.sqlite')
cur = connection.cursor()
while True:
    user_input = get_valid_input(
        '\nEnter (1) - Add a product: '
        '\nEnter (2) - Update a product: '
        '\nEnter (3) - Delete a product: '
        '\nEnter (4) - Show all Products: '
        '\nEnter (5) - To Exit: ',['1','2','3','4', '5'])
        
    if user_input == '1':
        add_product(cur)
    elif user_input == '2':
        update_product(cur)
    elif user_input == '3':
        delete_product(cur)
    elif user_input == '4':
        show_all(cur)
    elif user_input == '5':
        connection.commit()
        cur.close()
        break