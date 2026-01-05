from tabulate import tabulate
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# ----- SALES REPORT -----

# Revenue Report
def total_revenue(cur, pd):
    print('\n--- Total Sales Revenue ---')
    data = pd.read_sql_query('SELECT Sales.product_id, Products.price, Sales.quantity_sold FROM Sales JOIN Products ON Sales.product_id = Products.id', cur.connection)
    if data.empty:
        raise ValueError('\nNo sales found in the database.')
    else:
        total_revenue = (data['price'] * data['quantity_sold']).sum()
        total_items = (data['quantity_sold']).sum()
        print(f'\nTotal Revenue: {total_revenue:,.2f}€')
        print(f'\nTotal Products Sold: {total_items}')

def total_orders(cur):
    print('\n--- Total Orders ---\n')
    cur.execute('SELECT COUNT(*) FROM Sales')
    sale = cur.fetchone()
    if sale[0] == 0:
        raise ValueError ('\nNo sales found in the database.')
    else:
        print(f'Total sales: {sale[0]}')

# Best seller by quantity 
def best_seller(cur, pd):
    title = ' Three Most Sold Products '
    print('\n' + title.center(50, '-'))
    data = pd.read_sql_query('SELECT Products.name, Products.price, Sales.quantity_sold FROM Sales JOIN Products ON Sales.product_id = Products.id', cur.connection)
    if data.empty:
        raise ValueError('\nNo products found in the database.')
    else:
        top_three_best_seller = (data.groupby(['name', 'price'])['quantity_sold'].sum().reset_index().sort_values(by=['quantity_sold','price'], ascending=[False, False]).head(3))
        print(tabulate(top_three_best_seller, headers='keys', tablefmt='simple_grid', showindex=False))      

# ----- INVENTORY REPORT -----

# Stock report
def stock_report(cur, pd):
    title = ' STOCK REPORT (DESC) '
    print(f'\n' + title.center(50, '-'))
    data = pd.read_sql_query('SELECT name, stock_qty FROM Products', cur.connection)
    if data.empty:
        raise ValueError('\nNo products found in the database.')
    else:
        stock = data.sort_values(by=['stock_qty'], ascending = False)
        print(tabulate(stock, headers='keys', tablefmt='simple_grid', showindex=False))

# low-stock alert
def low_stock_report(cur, pd):
    title = ' LOW STOCK REPORT '
    print(f'\n' + title.center(60, '-'))
    data = pd.read_sql_query('SELECT name, stock_qty FROM Products', cur.connection)
    if data.empty:
        raise ValueError('\nNo products found in the database.')
    else:
        data['Availability'] = ''
        data.loc[data['stock_qty'] < 50, 'Availability'] = 'LOW STOCK'
        
        low_stock = data[data['stock_qty'] <50]
        if low_stock.empty:
            print('\nNo products with low stock was found.')
        else:
            print(tabulate(low_stock, headers = 'keys', tablefmt='simple_grid', showindex=False))

# ----- SUPPLIER REPORT -----

# List of active suppliers
def active_suppliers(cur, pd):
    print('\n--- Active Suppliers ---')
    supplier_info = pd.read_sql_query('SELECT name,contact FROM Suppliers', cur.connection)
    if supplier_info.empty:
        print('\nNo Suppliers found in the database.')
    else:
        print('\n' + tabulate(supplier_info, headers='keys', tablefmt='simple_grid', showindex=False))


def supplier_product_coverage(cur, pd):
    print('\n--- Suppliers connected to products ---\n')
    supplier_info = pd.read_sql_query('''SELECT Suppliers.name, COUNT(SupplierProducts.product_id) AS product_count
                                         FROM Suppliers LEFT JOIN SupplierProducts 
                                         ON Suppliers.id = SupplierProducts.supplier_id
                                         GROUP BY Suppliers.name
                                         ORDER BY product_count DESC
                                         ''', cur.connection)
    if supplier_info.empty:
        raise ValueError('\nNo Suppliers found in the database.')
    else:
        headers = ['Supplier Name','Number of Products']
        print('\n' + tabulate(supplier_info, headers=headers, tablefmt='simple_grid', showindex=False))


def products_without_supplier(cur, pd):
    print('\n--- Products without Supplier ---\n')
    products = pd.read_sql_query('SELECT DISTINCT id, name FROM Products WHERE id NOT IN (SELECT product_id FROM SupplierProducts) ORDER BY name ASC', cur.connection)
    if products.empty:
        print('\nNo products found in the database.')
    else:
        print('\n' + tabulate(products, headers='keys', tablefmt='simple_grid', showindex=False))

def sales_trend(cur, pd):
    sales_by_date = pd.read_sql_query('''SELECT DATE(sale_date) AS sale_day, SUM(quantity_sold * price) as total_sales
                                         FROM Sales LEFT JOIN Products
                                         ON Sales.product_id = Products.id
                                         GROUP BY sale_day''', cur.connection)
    sales_by_date['sale_day'] = pd.to_datetime(sales_by_date['sale_day'])
    sales_by_date = sales_by_date.set_index('sale_day')
    sales_by_date = (sales_by_date.resample('D').sum().fillna(0))
    sales_by_date.index.name = 'sale_day'

    plt.figure(figsize=(10,6))

    plt.plot(sales_by_date.index, sales_by_date['total_sales'], marker = 'o')

    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax.set_xlim(sales_by_date.index.min(), sales_by_date.index.max())
    plt.xticks(rotation=45)
    plt.title('Total Sales Per Day')
    plt.xlabel('Date')
    plt.ylabel('Sales (€)')
    plt.grid()
    plt.tight_layout()
    plt.show()