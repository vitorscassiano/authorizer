from typing import List, Optional
from authorizer.domain.account import Account


def is_empty(store: List[Account]):
    return bool(len(store) <= 0)

def save(store: List[Account], account: Account) -> None:
    store = [account]

def find(store: List[Account], account: Account) -> Optional[Account]:
    return filter(lambda c: c == acccount, store)
