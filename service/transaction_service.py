from ast import Store
from service.db_service import get_db_values, write_to_db
from store.user_store import UserStore
from utils import Transactions


def show_transaction_options():
    user = UserStore.get_user()
    while True:
        print("Login Successful")
        print("Transaction Options")
        print("1. ATM Withdrawal")
        print("2. Deposit")
        print("3. Transfer")
        print("4. Show All transactions")
        print("5. Show Top Customers")
        print("0. Quit")
        option = int(input("Kindly enter option: "))
        if option == 1:
            withdraw(user)
        elif option == 2:
            deposit(user)
        elif option == 3:
            transfer(user)
        elif option == 4:
            show_all_transactions(user)
        elif option == 5:
            show_top_customers()
        elif option == 0:
            exit()


def show_top_customers():
    no_of_customers = int(input("Enter how many number of top customers to fetch"))
    db_values = get_db_values()
    customers = db_values["users"]["data"]
    customers = sorted(customers, key=lambda d: d["balance"], reverse=True)[
        0:no_of_customers
    ]
    count = 1
    for customer in customers:
        print("Top Customers")
        print(f"{count} Name: {customer['name']}")
        print("-------------------------------------")
        count += 1


def withdraw(user, amount=None, transaction=True):
    if amount is None:
        amount = int(input("Enter the Amount to withdraw "))

    debit_amount = user["balance"] - amount
    if debit_amount < 1000:
        print("Insuffecient funds")
        return False
    user["balance"] = debit_amount
    print(debit_amount)
    print(user["balance"])

    db_values = get_db_values()
    for _user in db_values["users"]["data"]:
        if _user["customer_id"] == user["customer_id"]:
            _user["balance"] = user["balance"]
    if transaction:
        t = Transactions.WITHDRAW
        db_values = store_transaction(db_values, t.value, user, amount)
    print(db_values["users"]["data"])
    write_to_db(db_values)
    return True


def deposit(user, amount=None, transaction=True):
    if amount is None:
        amount = int(input("Enter the Amount to deposit "))

    credit_amount = user["balance"] + amount
    user["balance"] = credit_amount
    db_values = get_db_values()
    for _user in db_values["users"]["data"]:
        if _user["customer_id"] == user["customer_id"]:
            _user["balance"] = user["balance"]
    if transaction:
        t = Transactions.DEPOSIT
        db_values = store_transaction(db_values, t.value, user, amount)

    write_to_db(db_values)


def transfer(user):
    while True:
        account_number = input("Input Account number to transfer: ")
        if account_number == user["account_number"]:
            print("Cannot transfer to your own account")
            continue
        amount = int(input("Amount to transfer"))
        benefeciary = None
        db_values = get_db_values()
        for _user in db_values["users"]["data"]:
            if _user["account_number"] == account_number:
                benefeciary = _user
                break
        if benefeciary == None:
            print("Benefeciary not found. Try again")
            continue
        break

    can_withdraw = withdraw(user, amount, False)
    if not can_withdraw:
        print("Insuffecient funds")
        return
    deposit(benefeciary, amount, False)
    t = Transactions.TRANSFER
    db_values = get_db_values()
    db_values = store_transaction(db_values, t.value, user, amount)

    write_to_db(db_values)


def store_transaction(values, type, user, amount):
    last_id = values["transactions"]["last_transaction_id"]
    transaction_obj = {
        "id": last_id + 1,
        "type": type,
        "user_id": user["customer_id"],
        "amount": amount,
        "balance": user["balance"],
    }
    values["transactions"]["data"].append(transaction_obj)
    return values


def show_all_transactions(user):
    db_values = get_db_values()
    transactions = []
    for transaction in db_values["transactions"]["data"]:
        if transaction["user_id"] == user["customer_id"]:
            transactions.append(transaction)

    for transaction in transactions:
        print("Transactions")
        print(f"ID: {transaction['id']}")
        print(f"Type: {transaction['type']}")
        print(f"Amount: {transaction['amount']}")
        print(f"Balance: {transaction['balance']}")
        print("-------------------------------------")
