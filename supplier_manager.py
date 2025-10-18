from product_manager import get_valid_input, get_alphabetic_input, get_positive_number
from email_validator import validate_email, EmailNotValidError

def get_valid_email():
    while True:
        try:
            mail = input('\nEnter a valid mail: ')
            valid = validate_email(mail, check_deliverability=False)
            return valid.email   
        except EmailNotValidError as error:
            print('Invalid Email: ', error)

def add_supplier(cur):
    supplier_name = input('\nEnter suppliers name: ')
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
            supplier_name = input('\nPlease type a new name: ')
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