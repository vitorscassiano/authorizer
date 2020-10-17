from typing import List, Optional
from collections import defaultdict

ACCOUNTS = "accounts"
TRANSACTIONS = "transactions"


class MemoryRepository:
    def __init__(self, storage=defaultdict(list)):
        self.storage = storage

    def save_account(self, account):
        self.storage["account"] = [account]

    def save_transaction(self, transaction):
        self.storage[TRANSACTIONS] = self.storage[TRANSACTIONS] + \
            [transaction]

    def is_account_empty(self):
        return bool(len(self.storage["account"]) <= 0)

    def find_account(self):
        accounts = self.storage["account"]
        return accounts[0] if 0 < len(accounts) else None

    def find_all_transactions(self):
        return self.storage[TRANSACTIONS]

    def clean(self):
        self.storage = defaultdict(list)
