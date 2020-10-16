import sys
import json
from authorizer.application.controllers import (
    account_controller,
    transaction_controller
)

def main():
    for line in sys.stdin:
        data = json.loads(line.rstrip())
        if("account" in data):
            response = account_controller.handler(data)
            print(json.dumps(response))
        elif("transaction" in data):
            response = transaction_controller.handler(data)
            print(json.dumps(response))
        else:
            print("something wrong.")

if(__name__ == "__main__"):
    main()
