from src.product_manager import add_product, update_product, delete_product, show_all
from src.helpers import get_valid_input
from src.sales_manager import record_sale, show_sales
from src.supplier_manager import add_supplier, update_supplier, delete_supplier, assign_products_to_supplier, show_all_suppliers
from src.reports_manager import total_revenue, best_seller, sales_trend, total_orders, stock_report, low_stock_report, active_suppliers, supplier_product_coverage, products_without_supplier
from src.export_manager import export_data

###  PRODUCT MENU

def product_menu(cur):
    print('\n--- Product Menu ---')
    print('\n1) Add Product'
          '\n2) Update Product'
          '\n3) Delete Product'
          '\n4) Show Product List')
    user_input = get_valid_input('\nEnter Choice: ',['1','2','3','4'])
    if user_input == '1':
        add_product(cur)
    elif user_input == '2':
        update_product(cur)
    elif user_input == '3':
        delete_product(cur)
    else:
        show_all(cur)

### SALES MENU

def sales_menu(cur, pd):
    print('\n--- Sales Menu ---')
    print('\n1) Record Sale'
          '\n2) Show Sales')
    user_input = get_valid_input('\nEnter Choice: ',['1', '2'])
    if user_input == '1':
        record_sale(cur, pd)
    else: 
        show_sales(cur, pd)

### SUPPLIER MENU

def supplier_menu(cur, pd):
    print('\n--- Supplier Menu ---')
    print('\n1) Add Supplier'
          '\n2) Update Supplier'
          '\n3) Delete a Supplier'
          '\n4) Assign products to Suppliers'
          '\n5) Show all Suppliers')
    user_input = get_valid_input('\nEnter Choice: ',['1','2','3','4','5'])
    if user_input == '1':
        add_supplier(cur)
    elif user_input == '2':
        update_supplier(cur)
    elif user_input == '3':
        delete_supplier(cur)
    elif user_input == '4':
        assign_products_to_supplier(cur, pd)
    else:
        show_all_suppliers(cur)

### REPORTS MENU

def reports_menu(cur, pd):
    print('\n--- Reports & Analytics Menu ---')
    print('\n1) Sales Report'
          '\n2) Inventory Report'
          '\n3) Supplier Report'
          '\n4) Export Data')
    user_input = get_valid_input('\nEnter Choice: ',['1','2','3','4'])
    
    if user_input == '1':
        print('\n--- Sales Reports Menu ---')
        print('\n1) Total Sales Revenue'
              '\n2) Best Seller products'
              '\n3) Sales Trend'
              '\n4) Total Orders')
        sales_report = get_valid_input('\nEnter Choice: ',['1','2','3','4'])
        if sales_report == '1':
            total_revenue(cur, pd)
        elif sales_report == '2':
            best_seller(cur, pd)
        elif sales_report == '3':
            sales_trend(cur, pd)
        else:
            total_orders(cur)

    elif user_input == '2':
        print('\n--- Inventory Report Menu ---')
        print('\n1) Inventory Stock Report'
              '\n2) Low Stock Report ')
        inventory_report = get_valid_input('\nEnter Choice: ',['1','2'])
        if inventory_report == '1':
            stock_report(cur, pd)
        else:
            low_stock_report(cur, pd)

    elif user_input == '3':
        print('\n--- Supplier Report Menu ---')
        print('\n1) Supplier info'
              '\n2) Products per Supplier'
              '\n3) Show products without Supplier')
        supplier_report = get_valid_input('\nEnter Choice: ',['1','2','3'])
        if supplier_report == '1':
            active_suppliers(cur, pd)
        elif supplier_report == '2':
            supplier_product_coverage(cur, pd)
        else:
            products_without_supplier(cur, pd)
        
    else: 
        export_data(cur, pd)