from email_validator import validate_email, EmailNotValidError

# Valid input
def get_valid_input(prompt, options):
    while True:
        user_input = input(prompt).strip().lower()
        if user_input not in options:
            print('\nInvalid input. Please try again')
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
            print('Please type a price')

# Alphabetic input validation
def get_alphabetic_input(prompt):
    while True:
        user_input = input(prompt)
        if user_input.isalpha():
            return user_input.title()
        else:
            print("Input shouldn't contain numbers. Please type again")

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