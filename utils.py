from enum import Enum
import random


class Transactions(Enum):
    WITHDRAW = 1
    DEPOSIT = 2
    TRANSFER = 3


def generate_random(length: int):
    res = ""
    for i in range(length):
        res += str(random.random() * 100)[-1]
    return res
