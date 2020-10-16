from typing import List, Optional
from authorizer.domain.transaction import Transaction

from authorizer.domain.account import Account


def is_empty(store: List[Transaction]):
    return bool(len(store) <= 0)

def save(store: List[Transaction], transaction: Transaction) -> None:
    store = [transaction]

def find(store: List[Transaction], transaction: Transaction) -> Optional[Transaction]:
    return filter(lambda t: t == transaction, store)
