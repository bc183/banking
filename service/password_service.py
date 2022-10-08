def validatePassword(password: str):
    min_length = 6
    lower_case = 2
    upper_case = 2
    numbers = 2
    if len(password) < min_length:
        return False
    for i in password:
        if i.isupper():
            upper_case -= 1
        elif i.isdigit():
            numbers -= 1
        elif i.islower():
            lower_case -= 1
    return lower_case <= 0 and upper_case <= 0 and numbers <= 0


def encrypt_password(password: str):
    encrypt_password = ""
    for i in password:
        encrypted = ord(i) + 1
        if encrypted == 91:
            encrypted = 65
        if encrypted == 123:
            encrypted = 97
        encrypt_password += str(encrypted) + "_"

    return encrypt_password[: len(encrypt_password) - 1]


def decrypt_password(password: str):
    decrypt_password = ""
    passwords = password.split("_")
    for i in range(len(passwords)):
        order = int(passwords[i])
        print(order)
        original_order = order - 1
        if order == 65:
            original_order = 90
        elif order == 123:
            original_order = 96
        decrypt_password += chr(original_order)

    return decrypt_password
