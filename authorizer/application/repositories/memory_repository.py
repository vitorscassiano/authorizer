from typing import List, Optional
from collections import defaultdict


class MemoryRepository:
    def __init__(self, storage=defaultdict(list)):
        self.storage = storage

    def save(self, key, value):
        self.storage[key] = self.storage[key] + [value]

    def save_account(self, account):
        self.save("account", account)

    def save_transaction(self, transaction):
        self.save("transaction", transaction)

    def is_account_empty(self):
        return bool(self.storage["account"] <= 0)

    def find_account_by(self, account):
        return filter(lambda a: a == account, self.storage)

    def find_transaction_by(self, transaction):
        return filter(lambda t: t == transaction, self.storage)

    def find_all_transaction(self):
        return self.storage["transactions"]
