from service.db_service import get_db_values, write_to_db
from service.password_service import (
    decrypt_password,
    encrypt_password,
    validatePassword,
)
from service.transaction_service import show_transaction_options
from store.user_store import UserStore
from utils import generate_random


def login():
    db_values = get_db_values()
    users = db_values["users"]["data"]
    logged_in_user = None
    while True:
        customer_id = input("Enter Customer ID")
        password = input("Enter Password")
        is_login = False
        for user in users:
            if user["customer_id"] == int(customer_id):
                decrypted = decrypt_password(user["password"])
                print(decrypted)
                if decrypted == password:
                    logged_in_user = user
                    is_login = True
                    break
        if not is_login:
            print("Invalid login credentials")
            print(
                "Do you want to try again ? 1 for yes 2 for creating new user 3 for exit"
            )
            option = int(input())
            if option == 1:
                continue
            elif option == 2:
                create_user()
            else:
                exit()
        break
    UserStore.set_user(logged_in_user)
    show_transaction_options()


def create_user():
    customer_name = input("Enter Customer Name")
    password = None
    confirm_password = None
    while True:
        password = input("Enter Password")
        confirm_password = input("Enter Password again")

        if password != confirm_password:
            print("Passwords don't match")
            continue

        is_password_valid = validatePassword(password)
        if not is_password_valid:
            print(
                "Passwords should contain atleast 6 letter, 2 Uppercase 2 Lowercase and 2 Numbers"
            )
            continue
        break

    db_values = get_db_values()
    customer_id = db_values["users"]["last_customer_id"] + 1
    account_number = generate_random(10)
    encrypted_password = encrypt_password(password)
    user_obj = {
        "name": customer_name,
        "customer_id": customer_id,
        "password": encrypted_password,
        "account_number": account_number,
        "balance": 1000,
        "transactions_performed": 0,
    }
    db_values["users"]["data"].append(user_obj)
    db_values["users"]["last_customer_id"] += 1
    write_to_db(db_values)
    print("User created, Kindly login")
    login()
