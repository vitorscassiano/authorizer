import sys
import json
from authorizer.application.controllers import (
    account_controller,
    transaction_controller
)


def read_json(line):
    try:
        obj = json.loads(line)
        return obj
    except json.JSONDecodeError as e:
        print(e)


if(__name__ == "__main__"):
    for line in sys.stdin:
        data = read_json(line.rstrip())
        if("account" in data):
            response = account_controller.handler(data)
            print(response)
        elif("transaction" in data):
            response = transaction_controller.handler(data)
            print(response)
        else:
            print("something wrong.")
