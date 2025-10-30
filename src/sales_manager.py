from src.helpers import get_positive_number, get_valid_input
from datetime import datetime
from tabulate import tabulate

def record_sale(cur, pd):
    active_products = pd.read_sql_query('SELECT * FROM Products WHERE stock_qty > 0', cur.connection)
    if active_products.empty:
        print('\nNo products found.')
        return
    else:
        title = ' Active Products '
        print(f'\n' + title.center(80, '-'))
        print(tabulate(active_products, headers='keys', tablefmt='simple_grid', showindex= False))
    product_id = get_positive_number('\nEnter the id of the product you want to buy: ')
    cur.execute('SELECT * FROM Products WHERE id = ?',(product_id, ))
    row = cur.fetchone()

    if row is None:
        print("\nProduct doesn't exist!")
        return
    else:
        while True:
            quantity_sold = get_positive_number(f'\nPlease enter the quantity you want to buy for the product {row[1]}: ') 
            if quantity_sold == 0:
                print('\nQuantity cant be zero. Please try again!')
                continue
            if quantity_sold > row[4]:
                print(f'\nNot enough quantity. The available stock for the product is: {row[4]}. Please try again!')
                continue
            else:
                print(f'\nThe total cost of your order is: {row[3] * quantity_sold:.2f}€')
                sale_confirmation = get_valid_input('\nDo you want to proceed with the order? (y/n): ',['y','n'])
                if sale_confirmation == 'n':
                    print('\nOrder canceled.')
                    break
                else:
                    order_date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                    cur.execute('INSERT INTO Sales (product_id, quantity_sold, sale_date) VALUES (?,?,?)',(row[0],quantity_sold,order_date))
                    updated_stock = row[4] - quantity_sold
                    cur.execute('UPDATE Products SET stock_qty = ? WHERE id = ?',(updated_stock, row[0]))
                    print(f'\nSale recorded successfully! Remaining stock: {updated_stock:.0f} pieces')
                    cur.connection.commit()
                    break

def show_sales(cur, pd):
    sales = pd.read_sql_query('SELECT Sales.id, Products.name, Sales.quantity_sold, Sales.sale_date FROM Sales JOIN Products ON Sales.product_id = Products.id', cur.connection)
    sales['sale_date'] = pd.to_datetime(sales['sale_date']).dt.strftime('%Y-%m-%d %H:%M')
    if sales.empty:
        print('No sales found.')
        return
    else:
        title = ' All Time Sales '
        print(f'\n' + title.center(74, '-'))
        print(tabulate(sales, headers='keys', tablefmt='simple_grid', showindex= False))
        