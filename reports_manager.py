from tabulate import tabulate

# ----- SALES REPORT -----

# Revenue Report
def total_revenue(pd, connection):
    print('\n--- TOTAL SALES REVENUE ---')
    data = pd.read_sql_query('SELECT Sales.product_id, Products.price, Sales.quantity_sold FROM Sales JOIN Products ON Sales.product_id = Products.id', connection)
    if data.empty:
        raise ValueError('\nNo sales found.')
    else:
        total_revenue = (data['price'] * data['quantity_sold']).sum()
        total_items = (data['quantity_sold']).sum()
        print(f'\nTotal Revenue: {total_revenue:,.2f}€')
        print(f'\nTotal Items Sold: {total_items}')

def total_orders(cur):
    cur.execute('SELECT COUNT(*) FROM Sales')
    sale = cur.fetchone()
    if sale[0] == 0:
        raise ValueError ('\nNo sales found.')
    else:
        print(f'\nThe total sales are: {sale[0]}')

# Best seller by quantity 
def best_seller(pd, connection):
    title = ' Three Most Sold Products '
    print('\n' + title.center(50, '-'))
    data = pd.read_sql_query('SELECT Products.name, Products.price, Sales.quantity_sold FROM Sales JOIN Products ON Sales.product_id = Products.id', connection)
    if data.empty:
        raise ValueError('\nNo products found.')
    else:
        top_three_best_seller = (data.groupby(['name', 'price'])['quantity_sold'].sum().reset_index().sort_values(by=['quantity_sold','price'], ascending=[False, False]).head(3))
        print(tabulate(top_three_best_seller, headers='keys', tablefmt='simple_grid', showindex=False))      

# ----- INVENTORY REPORT -----

# Stock report
def stock_report(pd, connection):
    title = ' STOCK REPORT (DESC) '
    print(f'\n' + title.center(50, '-'))
    data = pd.read_sql_query('SELECT name, stock_qty FROM Products', connection)
    if data.empty:
        raise ValueError('\nNo products found.')
    else:
        stock = data.sort_values(by=['stock_qty'], ascending = False)
        print(tabulate(stock, headers='keys', tablefmt='simple_grid', showindex=False))

# low-stock alert
def low_stock_report(pd, connection):
    title = ' LOW STOCK REPORT '
    print(f'\n' + title.center(60, '-'))
    data = pd.read_sql_query('SELECT name, stock_qty FROM Products', connection)
    if data.empty:
        raise ValueError('\nNo products found.')
    else:
        data['Availability'] = ''
        data.loc[data['stock_qty'] < 50, 'Availability'] = 'LOW STOCK'
        
        low_stock = data[data['stock_qty'] <50]
        if low_stock.empty:
            print('\nNo low stock products!')
        else:
            print(tabulate(low_stock, headers = 'keys', tablefmt='simple_grid', showindex=False))


# ----- SUPPLIER REPORT -----

# List of active suppliers
def active_suppliers(connection, pd):
    supplier_info = pd.read_sql_query('SELECT name,contact FROM Suppliers', connection)
    if supplier_info.empty:
        print('\nNo Suppliers found.')
    else:
        print('\n' + tabulate(supplier_info, headers='keys', tablefmt='simple_grid'))


def supplier_product_coverage(connection, pd):
    supplier_info = pd.read_sql_query('''SELECT Suppliers.name, COUNT(SupplierProducts.product_id) AS product_count
                                         FROM Suppliers LEFT JOIN SupplierProducts 
                                         ON Suppliers.id = SupplierProducts.supplier_id
                                         GROUP BY Suppliers.name
                                         ORDER BY product_count DESC
                                         ''', connection)
    if supplier_info.empty:
        raise ValueError('\nNo Suppliers found')
    else:
        headers = ['Supplier Name','Number of Products']
        print('\n' + tabulate(supplier_info, headers=headers, tablefmt='simple_grid', showindex=False))


def products_without_supplier(connection, pd):
    products = pd.read_sql_query('SELECT DISTINCT id, name FROM Products WHERE id NOT IN (SELECT product_id FROM SupplierProducts) ORDER BY name ASC', connection)
    if products.empty:
        print('\nNo products found.')
    else:
        print('\n' + tabulate(products, headers='keys', tablefmt='simple_grid', showindex=False))
