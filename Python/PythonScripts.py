# ================================================================
# PYTHON SCRIPT: Banking Data Structure Demonstration
# ================================================================
# Demonstrates:
#   • List, Tuple, Set, Dictionary operations, and conversions
#   • Reading / writing CSV files
#   • Filtering, adding, removing, and checking customers
#   • Relational link with transactions.csv
# ================================================================

import csv
import os
import re
import datetime
import calendar


# ----------------------------------------------------------
# STEP 1: Read CSV files
# ----------------------------------------------------------
def read_csv(filename):
    """Read CSV and return list of dicts."""
    data = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
        print(f" Loaded {len(data)} records from {filename}")
        return data
    except FileNotFoundError:
        print(f" File not found: {filename}")
        return []


# ----------------------------------------------------------
# STEP 2: List Operations
# ----------------------------------------------------------
def list_operations(customers, transactions):
    """Demonstrates list creation, slicing, filtering, sorting, appending, and removing."""
    if not customers:
        print(" No customers loaded.")
        return
    print("\n=== LIST OPERATIONS ===")
    # Create simple lists for names and balances
    names = [c['name'] for c in customers]
    balances = [float(c['account_balance']) for c in customers]
    print(f"1. List of first 5 customer names: {names[:5]}")

    # Sort names alphabetically
    sorted_names = sorted(names)
    print(f"2. Sorted names (first 5): {sorted_names[:5]}")

    # Filter customers with balances above a threshold
    high_balances = [b for b in balances if b > 50000]
    print(f"3. Balances > 50000 (count): {len(high_balances)}")

    # Demonstrate appending new elements
    new_names = names.copy()
    new_names.append("New Customer")
    print(f"4. After appending 'New Customer' (last 3): {new_names[-3:]}")

    # Removing an element (pop removes by index)
    if new_names:
        new_names.pop(0)
        print(f"5. After removing first name (first 3): {new_names[:3]}")

    # Slicing part of a list (sublist)
    slice_balances = balances[5:10]
    print(f"6. Sliced balances (indices 5–9): {slice_balances}")

    # Display first few transaction amounts if available
    if transactions:
        tx_amounts = [float(t['amount']) for t in transactions]
        print(f"7. Transaction amounts (first 5): {tx_amounts[:5]}")

    print("=== END OF LIST OPERATIONS ===")


# ----------------------------------------------------------
# STEP 3: Tuple Operations
# ----------------------------------------------------------
def tuple_operations(customers, transactions):
    """
        Demonstrates how tuples work using customer and transaction data.
        Tuples are immutable and useful for fixed, ordered data.
    """
    if not customers:
        print(" No customers loaded.")
        return
    print("\n=== TUPLE OPERATIONS ===")
    # Create tuple for first customer
    first_customer = customers[0]
    cust_tuple = (first_customer['customer_id'], first_customer['name'], first_customer['city'])
    print(f"1. Customer tuple (ID, name, city): {cust_tuple}")

    # Accessing elements via index
    print(f"2. First element (customer_id): {cust_tuple[0]}")

    # Tuples cannot be modified (immutability)
    print("3. Tuples are immutable (cannot change elements)")

    # Converting tuple to list for modification
    cust_list = list(cust_tuple)
    cust_list.append("Extra")
    print(f"4. Converted to list and appended: {cust_list}")

    # Creating tuple of balances
    balance_tuple = tuple(float(c['account_balance']) for c in customers[:5])
    print(f"5. Tuple of first 5 balances: {balance_tuple}")

    # Creating tuple of transactions if available
    if transactions:
        tx_tuple = tuple((t['transaction_id'], t['customer_id'], t['amount']) for t in transactions[:3])
        print(f"6. Transaction tuple (ID, customer_id, amount, first 3): {tx_tuple}")

    print("=== END OF TUPLE OPERATIONS ===")


# ----------------------------------------------------------
# STEP 4: Set Operations
# ----------------------------------------------------------
def set_operations(customers, transactions):
    """
        Demonstrates set operations:
        Union, Intersection, Difference, Subset checks.
    """
    if not customers:
        print(" No customers loaded.")
        return
    print("\n=== SET OPERATIONS ===")
    # Create sets Unique city and branch sets
    cities = {c['city'] for c in customers}
    branches = {c['branch_code'] for c in customers}
    print(f"1. Unique cities (first 5): {list(cities)[:5]}")
    print(f"2. Unique branch codes: {branches}")

    # Perform union with transaction branch codes
    if transactions:
        tx_branches = {t['branch_code'] for t in transactions}
        all_branches = branches.union(tx_branches)
        print(f"3. Union of customer and transaction branches: {all_branches}")

    #  Intersection
    if transactions:
        common_branches = branches.intersection(tx_branches)
        print(f"4. Common branches in customers and transactions: {common_branches}")

    # Difference
    if transactions:
        customer_only_branches = branches.difference(tx_branches)
        print(f"5. Branches in customers but not transactions: {customer_only_branches}")

    # Subset check
    sample_cities = {'Mumbai', 'Delhi'}
    is_subset = sample_cities.issubset(cities)
    print(f"6. Is {sample_cities} a subset of cities? {is_subset}")

    print("=== END OF SET OPERATIONS ===")


# ----------------------------------------------------------
# STEP 5: Dictionary Operations
# ----------------------------------------------------------
def dictionary_operations(customers, transactions):
    """
        Demonstrates dictionary creation, lookup, update,
        aggregation, and nested structures.
    """
    if not customers:
        print(" No customers loaded.")
        return
    print("\n=== DICTIONARY OPERATIONS ===")

    # Create dictionary mapping IDs to names

    cust_dict = {c['customer_id']: c['name'] for c in customers}
    print(f"1. Customer ID to name (first 5): {dict(list(cust_dict.items())[:5])}")

    # Lookup a name by customer_id
    sample_id = customers[0]['customer_id']
    print(f"2. Name for customer ID {sample_id}: {cust_dict.get(sample_id, 'Not found')}")

    # Update dictionary entry
    cust_dict[sample_id] = cust_dict[sample_id] + " (Updated)"
    print(f"3. Updated name for ID {sample_id}: {cust_dict[sample_id]}")

    # Aggregation balances per branch
    branch_balances = {}
    for c in customers:
        branch = c['branch_code']
        balance = float(c['account_balance'])
        branch_balances[branch] = branch_balances.get(branch, 0) + balance
    print(f"4. Total balance per branch (first 3): {dict(list(branch_balances.items())[:3])}")

    # Transaction dictionary (if available)
    if transactions:
        tx_dict = {t['transaction_id']: float(t['amount']) for t in transactions}
        print(f"5. Transaction ID to amount (first 5): {dict(list(tx_dict.items())[:5])}")

    # Nested dictionary
    city_accounts = {}
    for c in customers:
        city = c['city']
        if city not in city_accounts:
            city_accounts[city] = []
        city_accounts[city].append(c['account_type'])
    print(f"6. City to account types (first 3): {dict(list(city_accounts.items())[:3])}")

    print("=== END OF DICTIONARY OPERATIONS ===")


# ----------------------------------------------------------
# STEP 6: Data Type Conversions
# ----------------------------------------------------------
def data_type_conversions(customers, transactions):
    if not customers:
        print(" No customers loaded.")
        return
    print("\n=== DATA TYPE CONVERSIONS ===")
    # List to Set (removes duplicates)
    cities_list = [c['city'] for c in customers]
    cities_set = set(cities_list)
    print(f"1. List to Set: Converted city list to set (unique cities, first 5): {list(cities_set)[:5]}")

    # List to Tuple (for immutability)
    balances_list = [float(c['account_balance']) for c in customers[:5]]
    balances_tuple = tuple(balances_list)
    print(f"2. List to Tuple: Converted first 5 balances to tuple: {balances_tuple}")

    # Set to List (sorting set items)
    branches_set = {c['branch_code'] for c in customers}
    branches_list = sorted(list(branches_set))
    print(f"3. Set to List: Converted branch codes set to sorted list: {branches_list}")

    # Dictionary to List
    cust_dict = {c['customer_id']: c['name'] for c in customers[:5]}
    cust_pairs = list(cust_dict.items())
    print(f"4. Dictionary to List: Converted customer ID-to-name dict to list of pairs: {cust_pairs}")

    # List to Dictionary
    name_balance_pairs = [(c['name'], float(c['account_balance'])) for c in customers[:5]]
    name_balance_dict = dict(name_balance_pairs)
    print(f"5. List to Dictionary: Converted name-balance pairs to dict: {name_balance_dict}")

    # Transaction conversions (if available)
    if transactions:
        tx_types_list = [t['transaction_type'] for t in transactions]
        tx_types_set = set(tx_types_list)
        tx_types_tuple = tuple(tx_types_set)
        print(f"6. List to Set to Tuple: Transaction types list to set to tuple: {tx_types_tuple}")

    print("=== END OF DATA TYPE CONVERSIONS ===")


# ----------------------------------------------------------
# STEP 7: Add New Customer
# ----------------------------------------------------------
def add_customer(customers, filename):
    """
        Allows the user to input and validate details for a new customer record.
        The record is appended both in memory and in the target CSV file.
        Validation covers: name, date, phone, email, balance, etc.
        """
    if not customers:
        print("Cannot add — no template data found.")
        return
    print("\n=== ADD NEW CUSTOMER ===")
    new_record = {}
    # Use the first customer as a template for fields
    fieldnames = customers[0].keys()

    # Validation functions
    def validate_name(value):
        return bool(re.match(r"^[A-Za-z\s'-]+$", value)) and not any(c.isdigit() for c in value)

    def validate_city_state(value):
        return bool(re.match(r"^[A-Za-z\s]+$", value)) and not any(c.isdigit() for c in value)

    def validate_gender(value):
        return value.lower() in ['m', 'f']

    def validate_account_type(value):
        return value.lower() in ['savings', 'current', 'fixed deposit']

    def validate_date_of_birth(value):
        """Validates date format, logical day/month, and ensures age > 18."""
        try:

            # Hardcode current date to October 11, 2025 for demo
            current_date = datetime.datetime(2025, 10, 11)
            date_obj = datetime.datetime.strptime(value, '%Y-%m-%d')

            # Calculate age
            age = current_date.year - date_obj.year - (
                        (current_date.month, current_date.day) < (date_obj.month, date_obj.day))

            # Validate month
            if not (1 <= date_obj.month <= 12):
                return False

            # Validate day for the month (considering leap years for February)
            days_in_month = calendar.monthrange(date_obj.year, date_obj.month)[1]
            if not (1 <= date_obj.day <= days_in_month):
                return False

            # Validate year < current year and age > 18
            return date_obj.year < current_date.year and age > 18
        except ValueError:
            return False

    def validate_phone_number(value):
        return bool(re.match(r"^\d{10}$", value))

    def validate_email(value):
        return bool(re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", value))

    def validate_branch_code(value):
        return bool(re.match(r"^BR\d{3}$", value))

    def validate_account_balance(value):
        try:
            balance = float(value)
            return balance >= 0
        except ValueError:
            return False

    # Field validation rules and prompts
    field_validators = {
        'name': (validate_name, "Enter name (e.g., Arjun Desai): "),
        'gender': (validate_gender, "Enter gender (M or F): "),
        'date_of_birth': (validate_date_of_birth, "Enter date of birth (e.g., 1990-01-01, age > 18, valid date): "),
        'city': (validate_city_state, "Enter city (e.g., Mumbai): "),
        'state': (validate_city_state, "Enter state (e.g., Maharashtra): "),
        'phone_number': (validate_phone_number, "Enter phone number (e.g., 9876543210): "),
        'email': (validate_email, "Enter email (e.g., user@example.com): "),
        'branch_code': (validate_branch_code, "Enter branch code (e.g., BR010): "),
        'account_type': (validate_account_type, "Enter account type (Savings, Current, Fixed Deposit): "),
        'account_balance': (validate_account_balance, "Enter account balance (e.g., 50000.00): ")
    }
    # -----------------------------
    # Input loop for each field
    # -----------------------------

    for key in fieldnames:
        if key == 'customer_id':
            # Generate next customer_id
            try:
                # Automatically assign next available ID
                max_id = max(int(c['customer_id']) for c in customers)
                new_record[key] = str(max_id + 1)
            except ValueError:
                print(" Error: Invalid customer_id values in data.")
                return
        else:
            validator, prompt = field_validators.get(key, (lambda x: True, f"Enter {key}: "))
            while True:
                value = input(prompt).strip()
                if validator(value):
                    new_record[key] = value
                    break
                else:
                    print(f" Invalid {key}. Please try again. ({prompt.strip()})")

    # Append the new record to the in-memory list
    customers.append(new_record)

    # Check if file exists and is empty; if so, write headers
    write_header = not os.path.exists(filename) or os.path.getsize(filename) == 0

    try:
        with open(filename, 'a', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if write_header:
                writer.writeheader()
            writer.writerow(new_record)
        print(" Customer added successfully to CSV!")

        # Verify the write by re-reading the file
        updated_customers = read_csv(filename)
        if any(c['customer_id'] == new_record['customer_id'] for c in updated_customers):
            print(f" Verified: Customer ID {new_record['customer_id']} found in {filename}.")
        else:
            print(f" Warning: Customer ID {new_record['customer_id']} not found in {filename} after write.")
    except PermissionError:
        print(f" Error: Permission denied when writing to {filename}.")
    except Exception as e:
        print(f" Error writing to {filename}: {str(e)}")


# ----------------------------------------------------------
# STEP 8: Remove Customer
# ----------------------------------------------------------
def remove_customer(customers, transactions, filename):
    """
       Removes a customer by ID after checking:
         • the ID exists
         • there are no related transactions
       Then rewrites the entire CSV file.
       """
    if not customers:
        print("No customers to remove.")
        return
    print("\n=== REMOVE CUSTOMER ===")
    customer_id = input("Enter customer ID to remove: ").strip()

    # Check if customer_id exists
    if not any(c['customer_id'] == customer_id for c in customers):
        print(f" Customer ID {customer_id} not found.")
        return

    # Check if customer has transactions
    if transactions and any(t['customer_id'] == customer_id for t in transactions):
        print(f" Cannot remove customer ID {customer_id}: Associated transactions exist.")
        return

    # Remove customer
    before = len(customers)
    customers[:] = [c for c in customers if c['customer_id'] != customer_id]
    print(f" Removed {before - len(customers)} record(s).")
    save_to_csv(customers, filename)


# ----------------------------------------------------------
# STEP 9: Check if Customer Exists
# ----------------------------------------------------------
def check_customer_exists(customers):
    """
        Search for customers based on field (name/city/type/gender/state)
        Uses case-insensitive substring matching.
        """
    if not customers:
        print(" No customers loaded.")
        return
    print("\n=== CHECK CUSTOMER EXISTS ===")
    print("Search by: (1) Name, (2) City, (3) Account Type, (4) Gender, (5) State")
    field = input("Enter choice (1–5): ").strip()
    query = input("Enter value to search: ").strip()

    # Validate query
    if not query:
        print(" Error: Search value cannot be empty.")
        return

    # Map numeric choice to actual field names
    field_map = {
        '1': 'name',
        '2': 'city',
        '3': 'account_type',
        '4': 'gender',
        '5': 'state'
    }

    search_field = field_map.get(field)
    if not search_field:
        print(" Invalid choice. Please enter a number between 1 and 5.")
        return

    # Use substring matching for all fields, case-insensitive
    matches = [c for c in customers if query.lower() in c.get(search_field, '').lower()]

    print(f"\n Searching for '{query}' in field '{search_field}' (case-insensitive)")
    if matches:
        print(f" Found {len(matches)} match(es):")
        for m in matches[:10]:
            print({k: m[k] for k in ['customer_id', 'name', 'city', 'account_type', 'account_balance']})
        if len(matches) > 10:
            print(f"... and {len(matches) - 10} more match(es) not displayed.")
    else:
        print(" No matches found.")


# ----------------------------------------------------------
# STEP 10: Filter Customers
# ----------------------------------------------------------
def filter_customers(customers):
    if not customers:
        return customers
    print("\n=== FILTER CUSTOMERS ===")
    print("1. By city")
    print("2. By account type")
    choice = input("Choose filter: ").strip()
    if choice == '1':
        city = input("Enter city: ").strip().lower()
        filtered = [c for c in customers if c['city'].lower() == city]
    elif choice == '2':
        acc = input("Enter account type (Savings/Current/Fixed Deposit): ").strip().lower()
        filtered = [c for c in customers if c['account_type'].lower() == acc]
    else:
        print("Invalid choice.")
        return customers
    # Sort filtered results by name in ascending order
    filtered = sorted(filtered, key=lambda c: c['name'])
    print(f" Found {len(filtered)} customers (sorted by name).")
    for f in filtered[:10]:
        print({k: f[k] for k in ['customer_id', 'name', 'city', 'account_type', 'account_balance']})
    return filtered


# ----------------------------------------------------------
# SAVE UTILITY
# ----------------------------------------------------------
def save_to_csv(customers, filename):
    with open(filename, 'w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=customers[0].keys())
        writer.writeheader()
        writer.writerows(customers)
    print(" CSV updated successfully.")


# ----------------------------------------------------------
# MAIN MENU
# ----------------------------------------------------------
if __name__ == "__main__":
    print("=== BANKING DATA STRUCTURE DEMONSTRATION ===")
    customers = read_csv("../Csv File/customers.csv")
    transactions = read_csv("../Csv File/transactions.csv")

    while True:
        print("\nSelect an option:")
        print("1. List Operations")
        print("2. Tuple Operations")
        print("3. Set Operations")
        print("4. Dictionary Operations")
        print("5. Data Type Conversions")
        print("6. Add New Customer")
        print("7. Remove Customer")
        print("8. Check if Customer Exists")
        print("9. Filter Customers")
        print("10. Exit")

        choice = input("Enter choice (1–10): ").strip()
        if choice == '1':
            list_operations(customers, transactions)
        elif choice == '2':
            tuple_operations(customers, transactions)
        elif choice == '3':
            set_operations(customers, transactions)
        elif choice == '4':
            dictionary_operations(customers, transactions)
        elif choice == '5':
            data_type_conversions(customers, transactions)
        elif choice == '6':
            add_customer(customers, "customers.csv")
        elif choice == '7':
            remove_customer(customers, transactions, "customers.csv")
        elif choice == '8':
            check_customer_exists(customers)
        elif choice == '9':
            customers = filter_customers(customers)
        elif choice == '10':
            print("\n Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 10.")