from database import init_db
from account import BankAccount


def create_account():
    name = input("Enter account holder name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return
    try:
        balance = float(input("Enter initial balance: "))
    except ValueError:
        print("Invalid balance.")
        return
    account = BankAccount(name, balance)
    account.save()
    print(f"Account created with ID {account.id}")


def deposit(account):
    try:
        amount = float(input("Enter deposit amount: "))
        account.deposit(amount)
        print(f"Deposited. New balance: {account.check_balance()}")
    except ValueError as e:
        print(e)


def withdraw(account):
    try:
        amount = float(input("Enter withdrawal amount: "))
        account.withdraw(amount)
        print(f"Withdrawn. New balance: {account.check_balance()}")
    except ValueError as e:
        print(e)


def check_balance(account):
    print(f"Balance: {account.check_balance()}")


def delete_account(account):
    account.delete()
    print("Account deleted.")


def select_account():
    accounts = BankAccount.get_all()
    if not accounts:
        print("No accounts found.")
        return None
    print("Accounts:")
    for acc in accounts:
        print(f"  ID {acc.id}: {acc.name} - {acc.check_balance()}")
    try:
        acc_id = int(input("Enter account ID: "))
    except ValueError:
        print("Invalid ID.")
        return None
    account = BankAccount.get_by_id(acc_id)
    if not account:
        print("Account not found.")
        return None
    return account


def main():
    init_db()

    while True:
        print()
        print("=" * 30)
        print("   Bank Account Simulator")
        print("=" * 30)
        print("1. Create account")
        print("2. Select account")
        print("3. Exit")
        print("=" * 30)
        print()
        choice = input("Choose option (1/2/3): ")

        if choice == "3":
            print("Goodbye!")
            break

        if choice == "1":
            create_account()
            continue

        if choice == "2":
            account = select_account()
            if not account:
                continue
            while True:
                print()
                print(f"Account: {account.name}")
                print("1. Deposit")
                print("2. Withdraw")
                print("3. Check balance")
                print("4. Delete account")
                print("5. Back to main menu")
                sub = input("Choose option: ")
                if sub == "1":
                    deposit(account)
                elif sub == "2":
                    withdraw(account)
                elif sub == "3":
                    check_balance(account)
                elif sub == "4":
                    delete_account(account)
                    break
                elif sub == "5":
                    break
                else:
                    print("Invalid option.")
            continue

        print("Invalid option.")


if __name__ == "__main__":
    main()
