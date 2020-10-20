import sys
import json
from authorizer.application.controllers import (
    create_account_handler,
    transaction_handler
)


def execute(line):
    data = json.loads(line.rstrip())
    if("account" in data):
        return create_account_handler(data)
    elif("transaction" in data):
        return transaction_handler(data)
    else:
        raise Exception("invalid-payload")


def main():
    for line in sys.stdin:
        try:
            response = execute(line)
            print(json.dumps(response))
        except Exception as e:
            print(json.dumps({"error": str(e)}))


if(__name__ == "__main__"):
    main()
