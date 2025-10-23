from product_manager import get_valid_input, get_positive_number
from email_validator import validate_email, EmailNotValidError
from tabulate import tabulate

def get_valid_email():
    while True:
        try:
            mail = input('\nEnter a valid mail: ')
            valid = validate_email(mail, check_deliverability=False)
            return valid.email   
        except EmailNotValidError as error:
            print('Invalid Email: ', error)

def products_ids_input():
    while True:
        product_id = input("\nEnter product id's to assign (comma-separated): ")
        product_ids = [p_id.strip() for p_id in product_id.split(',') if p_id.strip().isdigit()]

        if not product_ids:
            print('\nNo valid product ID entered.')
        else:
            product_ids = list(map(int, product_ids))
            return product_ids

def add_supplier(cur):
    supplier_name = input('\nEnter suppliers name: ').strip()
    supplier_contact = get_valid_email()
    cur.execute('INSERT OR IGNORE INTO Suppliers (name, contact) VALUES (?,?)',(supplier_name, supplier_contact))
    print('\nSupplier has been added successfully!')
    cur.connection.commit()

def delete_supplier(cur):
    supplier_id = get_positive_number('\nEnter the id of the supplier you want to delete: ')
    cur.execute('SELECT * FROM Suppliers WHERE id = ?',(supplier_id, ))
    row = cur.fetchone()

    if row is None:
        print("\nSupplier doesn't exist.")
        return
    else:
        cur.execute('DELETE FROM Suppliers WHERE id = ?',(row[0], ))
        print('\nSupplier has been deleted!')
        cur.connection.commit()

def update_supplier(cur):
    supplier_id = get_positive_number('\nEnter the id of the supplier you want to update: ')
    cur.execute('SELECT * FROM Suppliers WHERE id = ?',(supplier_id, ))
    row = cur.fetchone()

    if row is None:
        print("\nSupplier doesn't exist")
        return
    else:
        update_choice = get_valid_input('\nChoose which value you want to update (Name/Contact): ',['name','contact'])
        if update_choice == 'name':
            supplier_name = input('\nPlease type a new name: ').strip()
            cur.execute('UPDATE Suppliers SET name = ? WHERE id = ?',(supplier_name, row[0]))
            print('\nSupplier name has been updated!')
            cur.connection.commit()
        else:
            supplier_contact = get_valid_email()
            cur.execute('UPDATE Suppliers SET contact = ? WHERE id = ?',(supplier_contact, row[0]))
            print('\nSupplier contact information has been updated!')
            cur.connection.commit()

def show_all_suppliers(cur):
    print('\n--- Active Suppliers ---\n')
    cur.execute('SELECT * FROM SUPPLIERS')
    for rows in cur.fetchall():
        print(f'Supplier ID: {rows[0]} | Supplier Name: {rows[1]} | Supplier Contact: {rows[2]}')

def assign_products_to_supplier(cur, pd):
    supplier_data = pd.read_sql_query('SELECT name FROM SUPPLIERS', cur.connection)
    print("\nThe active suppliers are:\n")
    print(tabulate(supplier_data, headers='keys', tablefmt='simple_grid', showindex=False))

    valid_suppliers = supplier_data['name'].str.lower().tolist()
    user_input = get_valid_input('\nSelect a supplier to assign products: ',valid_suppliers)

    cur.execute('SELECT id FROM Suppliers WHERE LOWER(name) = ?', (user_input.lower(), ))
    supplier_id = cur.fetchone()
    if supplier_id is None:
        print('\nSupplier not found.')
        return
    else:
        supplier_id = supplier_id[0]

        data = pd.read_sql_query('SELECT * FROM PRODUCTS', cur.connection)
        print('\n' + tabulate(data, headers='keys', tablefmt='simple_grid', showindex=False))
        assigned_products = products_ids_input()
        if not assigned_products:
            print('\nNo products were assigned to supplier.')
            return
        else:
            updated = False

            for id in assigned_products:
                if id in data['id'].values:
                    cur.execute('INSERT OR IGNORE INTO SupplierProducts (supplier_id, product_id) VALUES (?,?)',(supplier_id, id)) 
                    updated = True
                else:
                    print("\nProduct id doesn't exist")

            if updated:
                print("\nID's have been updated!")
                cur.connection.commit()