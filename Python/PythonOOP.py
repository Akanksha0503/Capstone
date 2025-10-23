import csv
from datetime import datetime
from typing import Optional


class BankAccount:
    """
    Base class for a bank account (OOP: Encapsulation with private attributes).
    Represents a general account with deposit/withdraw functionality.
    """

    def __init__(self, account_id: str, customer_id: str, branch_code: str, initial_balance: float = 0.0):
        """
        Constructor: Initializes account attributes.
        OOP: Encapsulation - _balance is private.
        """
        self._account_id = account_id  # Private attribute
        self._customer_id = customer_id
        self._branch_code = branch_code
        self._balance = initial_balance
        self._transactions = []  # List to log transactions (ties to transactions table)
        print(
            f" BankAccount initialized: ID={self._account_id}, Customer={self._customer_id}, Initial Balance={self._balance:.2f}")

    def deposit(self, amount: float) -> bool:
        """
        Overridden deposit: Adds interest on deposit (OOP: Polymorphism).
        """
        print(f" SavingsAccount deposit called (polymorphism from BankAccount).")

        # Demo: Minimum deposit rule for failure simulation
        min_deposit = 200.0
        if amount < min_deposit:
            print(f" Savings accounts require minimum ${min_deposit} deposit. Amount {amount:.2f} too small.")
            return False

        print(f" BankAccount deposit called. Depositing ${amount:.2f}...")
        self._balance += amount
        print(f" Deposit successful. New balance: ${self._balance:.2f}")

        print(f"   OOP: Overridden method adds child-specific behavior.")
        return True

    def withdraw(self, amount: float) -> bool:
        """
        Withdraw method: Subtracts amount if sufficient funds.
        OOP: Validation logic in method.
        """
        if amount > 0 and amount <= self._balance:
            self._balance -= amount
            self._log_transaction('DEBIT', 'withdrawal', amount)
            print(f" Withdrew {amount:.2f} from {self._account_id}. New balance: {self.get_balance():.2f}")
            print(f"   OOP: Method enforces business rules (e.g., no overdraft).")
            return True
        else:
            print(" Insufficient funds or invalid amount.")
            print(f"   OOP: Encapsulation protects private _balance from invalid changes.")
            return False

    def transfer(self, other_account: 'BankAccount', amount: float) -> bool:
        """
        Transfer method: Demonstrates polymorphism when called on different account types.
        OOP: Interacts with other objects.
        """
        if self.withdraw(amount):
            if other_account.deposit(amount):
                print(f" Transferred {amount:.2f} from {self._account_id} to {other_account._account_id}.")
                print(f"   OOP: Polymorphism - deposit() behaves differently based on receiver type.")
                return True
            else:
                # Rollback if deposit fails
                self._balance += amount
                print(" Transfer failed - rolling back withdrawal.")
        return False

    def get_balance(self) -> float:
        """
        Getter method for balance (OOP: Encapsulation).
        """
        print(f"Accessing balance for {self._account_id} via getter method.")
        return self._balance

    def _log_transaction(self, transaction_type: str, category: str, amount: float):
        """
        Private method to log transactions (internal use only).
        Ties to transactions table schema.
        OOP: Private method for internal encapsulation.
        """
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        transaction = {
            'transaction_type': transaction_type,
            'category': category,
            'amount': amount,
            'date': timestamp,
            'account_id': self._account_id
        }
        self._transactions.append(transaction)
        print(f" Private _log_transaction called: {transaction_type} {amount:.2f} on {timestamp}")

    def get_account_info(self) -> dict:
        """
        Returns account details as dict (useful for CSV export).
        OOP: Public method exposing controlled data.
        """
        print(f" Getting account info for {self._account_id}.")
        return {
            'account_id': self._account_id,
            'customer_id': self._customer_id,
            'branch_code': self._branch_code,
            'balance': self._balance,
            'transaction_count': len(self._transactions)
        }

    def print_transaction_history(self):
        """
        Prints transaction log (demonstrates access to internal list).
        """
        print(f"\n Transaction History for {self._account_id}:")
        if not self._transactions:
            print("   No transactions yet.")
        for i, tx in enumerate(self._transactions, 1):
            print(f"   {i}. {tx['date']} - {tx['transaction_type']} {tx['category']} {tx['amount']:.2f}")


class SavingsAccount(BankAccount):
    """
    Extended class for Savings Account (OOP: Inheritance from BankAccount).
    Adds interest calculation (polymorphism: overrides deposit).
    """

    def __init__(self, account_id: str, customer_id: str, branch_code: str, initial_balance: float = 0.0,
                 interest_rate: float = 0.03):
        """
        Constructor: Calls parent constructor + savings-specific attribute.
        OOP: super() for inheritance.
        """
        super().__init__(account_id, customer_id, branch_code, initial_balance)
        self._interest_rate = interest_rate  # Private savings-specific attribute
        print(f" SavingsAccount initialized: {self._account_id} with {interest_rate * 100:.1f}% interest rate.")

    def deposit(self, amount: float) -> bool:
        """
        Overridden deposit: Adds interest on deposit (OOP: Polymorphism).
        """
        print(f" SavingsAccount deposit called (polymorphism from BankAccount).")
        if super().deposit(amount):  # Call parent deposit
            interest = amount * self._interest_rate
            self._balance += interest
            print(
                f" Added interest: {interest:.2f} (at {self._interest_rate * 100:.1f}% rate). Total balance: {self.get_balance():.2f}")
            print(f"   OOP: Overridden method adds child-specific behavior.")
            return True
        return False

    def calculate_annual_interest(self) -> float:
        """
        Savings-specific method: Calculates annual interest.
        OOP: Method unique to subclass (extension of inheritance).
        """
        annual_interest = self._balance * self._interest_rate
        print(f" Calculated annual interest for {self._account_id}: {annual_interest:.2f}")
        return annual_interest

    def get_account_info(self) -> dict:
        """
        Overridden: Adds interest rate to parent info (OOP: Polymorphism).
        """
        print(f" SavingsAccount get_account_info called (overridden from parent).")
        info = super().get_account_info()
        info['interest_rate'] = self._interest_rate
        info['annual_interest'] = self.calculate_annual_interest()
        return info


# Example Usage: Integrating with Banking Data (from CSV)
def load_customers_from_csv(filename: str) -> list:
    """
    Loads customers from CSV (as in the script).
    """
    customers = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                customers.append(row)
        print(f" Loaded {len(customers)} customers from CSV.")
    except FileNotFoundError:
        print(f" File not found: {filename}")
    return customers


# Interactive User Input Demo
def interactive_demo():
    """
    Interactive menu for user input to demonstrate OOP operations.
    """
    customers = load_customers_from_csv("customers.csv")

    if not customers:
        print("No customer data loaded. Create customers.csv first.")
        return

    # Create account objects
    first_customer = customers[0]
    basic_account = BankAccount(
        account_id="ACC001",
        customer_id=first_customer['customer_id'],
        branch_code=first_customer['branch_code'],
        initial_balance=1000.0
    )

    savings_account = SavingsAccount(
        account_id="SAV001",
        customer_id=first_customer['customer_id'],
        branch_code=first_customer['branch_code'],
        initial_balance=5000.0,
        interest_rate=0.05
    )

    accounts = {'1': basic_account, '2': savings_account}

    print("\n" + "=" * 60)
    print("=== INTERACTIVE OOP BANKING DEMO ===")
    print("Account( 1=Basic, 2=Savings ) " )
    print("=" * 60)

    while True:
        print("\nOperations:")
        print("1. Deposit")
        print("2. Withdraw")
        print("3. Transfer between accounts")
        print("4. View Balance")
        print("5. View Account Info")
        print("6. View Transaction History")
        print("7. Calculate Annual Interest (Savings only)")
        print("8. Exit")

        choice = input("Choose operation (1-8): ").strip()

        if choice == '8':
            print("\n Exiting interactive demo.")
            break

        if choice in ['1', '2', '4', '5', '6']:
            acc_choice = input("Select account (1=Basic, 2=Savings): ").strip()
            if acc_choice not in accounts:
                print(" Invalid account choice.")
                continue
            selected_account = accounts[acc_choice]
            acc_name = "Basic" if acc_choice == '1' else "Savings"

            if choice == '1':  # Deposit
                try:
                    amount = float(input("Enter deposit amount: "))
                    selected_account.deposit(amount)
                except ValueError:
                    print(" Invalid amount. Must be a number.")

            elif choice == '2':  # Withdraw
                try:
                    amount = float(input("Enter withdraw amount: "))
                    selected_account.withdraw(amount)
                except ValueError:
                    print(" Invalid amount. Must be a number.")

            elif choice == '4':  # View Balance
                print(f" {acc_name} Account Balance: {selected_account.get_balance():.2f}")

            elif choice == '5':  # View Account Info
                print(f" {acc_name} Account Info: {selected_account.get_account_info()}")

            elif choice == '6':  # View Transaction History
                selected_account.print_transaction_history()

        elif choice == '3':  # Transfer
            from_choice = input("From account (1=Basic, 2=Savings): ").strip()
            to_choice = input("To account (1=Basic, 2=Savings): ").strip()
            if from_choice not in accounts or to_choice not in accounts:
                print(" Invalid account choice.")
                continue
            try:
                amount = float(input("Enter transfer amount: "))
                from_acc = accounts[from_choice]
                to_acc = accounts[to_choice]
                from_acc.transfer(to_acc, amount)
            except ValueError:
                print(" Invalid amount. Must be a number.")

        elif choice == '7':  # Annual Interest (Savings only)
            if '2' in accounts:
                print(f"Annual Interest for Savings: {savings_account.calculate_annual_interest():.2f}")
            else:
                print(" No Savings account available.")

        else:
            print(" Invalid operation choice.")


# Demo: Create Account Objects (Non-interactive for quick test)
def quick_demo():
    """
    Quick non-interactive demo with hardcoded inputs.
    """
    customers = load_customers_from_csv("customers.csv")

    if customers:
        first_customer = customers[0]
        basic_account = BankAccount(
            account_id="ACC001",
            customer_id=first_customer['customer_id'],
            branch_code=first_customer['branch_code'],
            initial_balance=1000.0
        )

        savings_account = SavingsAccount(
            account_id="SAV001",
            customer_id=first_customer['customer_id'],
            branch_code=first_customer['branch_code'],
            initial_balance=5000.0,
            interest_rate=0.05  # 5% interest
        )

        # Hardcoded operations for demo
        print("\n" + "=" * 60)
        print("=== QUICK OOP BANKING DEMO (Hardcoded Inputs) ===")
        print("=" * 60)

        # Encapsulation demo
        print("\n DEMO: Encapsulation - Private Attribute Access")
        print(f"Proper access via getter: {basic_account.get_balance():.2f}")

        # Basic operations
        print("\n1. Basic BankAccount Operations:")
        basic_account.deposit(200.0)
        basic_account.withdraw(50.0)
        basic_account.print_transaction_history()

        # Savings operations
        print("\n2. SavingsAccount Operations:")
        savings_account.deposit(1000.0)
        savings_account.calculate_annual_interest()
        savings_account.print_transaction_history()

        # Transfer
        print("\n3. Transfer Demo:")
        basic_account.transfer(savings_account, 300.0)

        # Polymorphism loop
        print("\n4. Polymorphism Loop:")
        accounts = [basic_account, savings_account]
        for acc in accounts:
            print(f"\n--- {type(acc).__name__} ---")
            acc.deposit(100.0)
            print(f"Balance: {acc.get_balance():.2f}")

        print("\n" + "=" * 60)
        print("=== END OF QUICK DEMO ===")
        print("=" * 60)
    else:
        print("No customer data loaded.")


# Main execution
if __name__ == "__main__":
    print("Choose demo mode:")
    print("1. Interactive (User Input)")
    print("2. Quick (Hardcoded)")

    mode = input("Enter choice (1 or 2): ").strip()

    if mode == '1':
        interactive_demo()
    elif mode =='2':
        quick_demo()
    else:
        print("Invalid Input")