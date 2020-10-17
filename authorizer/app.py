import sys
import json

from authorizer.application.controllers import create_account_handler, transaction_handler


def main():
    for line in sys.stdin:
        data = json.loads(line.rstrip())
        if("account" in data):
            response = create_account_handler(data)
            print(json.dumps(response))
        elif("transaction" in data):
            response = transaction_handler(data)
            print(json.dumps(response))
        else:
            print("something wrong.")


if(__name__ == "__main__"):
    main()
