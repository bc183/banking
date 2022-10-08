from service.auth_service import create_user, login
from service.db_service import init_db


def start_app():
    # init db
    # init_db()
    # print inital options
    print("Welcome to Happy Bank. Kindly select one of the options,")
    print("1. Login")
    print("2. Create a new account")
    print("3. Exit")
    option = int(input())
    if option == 1:
        login()
    elif option == 2:
        # perform register
        create_user()
    elif option == 3:
        exit()


if __name__ == "__main__":
    start_app()
