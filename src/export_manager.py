from src.helpers import get_valid_input
from datetime import datetime
import os

def export_data(cur, pd):
    os.makedirs('exports', exist_ok=True)
    current_datetime = datetime.now().strftime('%Y-%m-%d_%H_%M')
    print('\n--- Data Export Menu ---')
    print('\n1) Export Products'
          '\n2) Export Sales'
          '\n3) Export Suppliers'
          '\n4) Export SupplierProducts')
    user_input = get_valid_input('\nEnter Choice: ',['1','2','3','4'])
    if user_input == '1':
        path = f'exports/products_export_{current_datetime}.csv'
        products_export = pd.read_sql_query('SELECT * FROM Products', cur.connection)
        products_export.to_csv(path, index = False)
        print(f'\nFile exported successfully: {path}')
    elif user_input == '2':
        path = f'exports/sales_export_{current_datetime}.csv'
        sales_export = pd.read_sql_query('SELECT * FROM Sales', cur.connection)
        sales_export.to_csv(path, index = False)
        print(f'\nFile exported successfully: {path}')
    elif user_input == '3':
        path = (f'exports/suppliers_export_{current_datetime}.csv')
        supplier_input = pd.read_sql_query('SELECT * FROM Suppliers', cur.connection)
        supplier_input.to_csv(path, index = False)
        print(f'\nFile exported successfully: {path}')
    else:
        path = (f'exports/supplierProducts_export_{current_datetime}.csv')
        supplierProducts_export = pd.read_sql_query('SELECT * FROM SupplierProducts', cur.connection)
        supplierProducts_export.to_csv(path, index = False)
        print(f'\nFile exported successfully: {path}')