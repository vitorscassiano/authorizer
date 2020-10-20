from typing import Optional, List
from collections import defaultdict
from authorizer.domain.account import Account
from authorizer.domain.transaction import Transaction

ACCOUNTS = "accounts"
TRANSACTIONS = "transactions"


class MemoryRepository:
    def __init__(self, storage=defaultdict(list)):
        self.storage = storage

    def save_account(self, account) -> None:
        self.storage[ACCOUNTS] = [account]

    def save_transaction(self, transaction) -> None:
        self.storage[TRANSACTIONS] = self.storage[TRANSACTIONS] + \
            [transaction]

    def find_account(self) -> Optional[Account]:
        accounts = self.storage[ACCOUNTS]
        return accounts[0] if 0 < len(accounts) else None

    def all_transactions(self) -> List[Transaction]:
        return self.storage[TRANSACTIONS]

    def clean(self) -> None:
        self.storage = defaultdict(list)
