from typing import List
from authorizer.domain.transaction import Transaction


class TransactionRepository:
    def __init__(self):
        self.db = []

    def is_empty(self, transaction: Transaction) -> None:
        self.db.append(transaction)

    def save(self, transaction: Transaction) -> None:
        self.db.append(transaction)

    def find(self, transaction: Transaction) -> Transaction:
        raise Exception("Does not implemented")

    def find_all(self) -> List[Transaction]:
        return self.db

    def remove(self, transaction: Transaction) -> None:
        raise Exception("Does not implemented")
