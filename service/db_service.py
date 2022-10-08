import json


def init_db():
    initial_values = {
        "users": {"data": [], "last_customer_id": 0},
        "transactions": {"data": [], "last_transaction_id": 0},
    }
    write_to_db(initial_values)


def write_to_db(values):
    with open("db.json", "w") as file:
        file.write(json.dumps(values))


def get_db_values():
    content = {}
    with open("db.json", "r") as file:
        content = json.loads(file.read())
    return content
