import sqlite3

# Valid input
def get_valid_input(prompt, options):
    while True:
        user_input = input(prompt).strip().lower()
        if user_input not in options:
            print('\nInvalid Input.')
        else:
            return user_input
        
# Positive numbers validation     
def get_positive_number(prompt):
    while True:
        try:
            user_input = float(input(prompt))
            if user_input < 0:
                print('The value cannot be below zero, please enter a positive value')
            elif user_input == 0:
                user_input = 0
                return user_input
            else:
                return user_input
        except ValueError:
            print('Please type a price.')

# Alphabetic input validation
def get_alphabetic_input(prompt):
    while True:
        user_input = input(prompt)
        if user_input.isalpha():
            return user_input.title()
        else:
            print("Input shouldn't contain numbers. Please type again!")
# Add product to the inventory
def add_product(cur):
    product_name = input('\nProduct Name: ').title()
    category_name = get_alphabetic_input('\nCategory Name: \n')
    price = get_positive_number('\nPrice: ')
    stock = get_positive_number('\nStock Quantity: ')
    cur.execute('''INSERT OR IGNORE INTO Products 
                (name, category, price, stock_qty) VALUES (?,?,?,?)''', (product_name, category_name, price, stock))
    print('\nProduct has been added in the inventory\n')
    cur.connection.commit()

# Update product
def update_product(cur):
    product_id = get_positive_number('\nEnter the id of the product you want to update: ')
    cur.execute('SELECT * FROM Products WHERE id = ?', (product_id, ))
    row = cur.fetchone()
    #print(row)
    if row is None:
        print("\nProduct doesn't exist.")
        return 
    else:
        update_choice = get_valid_input('\nChoose which value you want to update (Name/Category/Price/Stock): ',['name','category','price','stock'])
        if update_choice == 'name':
            name_update = input('\nPlease type the new name:  ').title()
            cur.execute('UPDATE Products SET name = ? WHERE id = ?',(name_update, row[0]))
            print('\nProduct name has been updated!')
        elif update_choice == 'category':
            category_update = get_alphabetic_input('\nPlease type the new category: ')
            cur.execute('UPDATE Products SET category = ? WHERE id = ?',(category_update, row[0]))
            print('\nProduct category has been updated!')
        elif update_choice == 'price':
            price_update = get_positive_number('\nPlease type the new price: ')
            cur.execute('UPDATE Products SET price = ? WHERE id = ?',(price_update, row[0]))
            print('\nPrice has been updated!')
        else:
            stock_update = get_positive_number('\nPlease type the updated stock: ')
            cur.execute('UPDATE Products SET stock_qty = ? WHERE id = ?',(stock_update, row[0]))
            print('\nStock has been updated!')
            cur.connection.commit()

# Delete product
def delete_product(cur):
    product_id = get_positive_number('\nEnter the id of the product you want to delete: ')
    cur.execute('SELECT * FROM Products WHERE id = ?',(product_id, ))
    row = cur.fetchone()

    if row is None:
        print("\nProduct doesn't exist!")
        return
    else:
        cur.execute('DELETE FROM Products WHERE id = ?',(row[0], ))
        print('\nThe product has been deleted!')
        cur.connection.commit()

# Show all products
def show_all(cur):
    print('\nAvailable Products: \n')
    cur.execute('SELECT * FROM PRODUCTS')

    for row in cur.fetchall():
        print(f'Product: {row[1]} | Category: {row[2]} | Price: {row[3]:.2f} | Available Stock: {row[4]}') 