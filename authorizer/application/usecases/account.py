from authorizer.application.repositories.storage import Storage
from authorizer.application.repositories.account_repository import AccountRepository
from authorizer.domain.account import Account

def save(store, data):
    store = [data]

def find(store, data):
    return filter(lambda d: d == data ,store)

def is_empty(store):
    return (len(store) <= 0)


def create_account(store, activeCard, availableLimit):
    if(is_empty(store)):
        account = Account(activeCard, availableLimit)
        save(store, account)
        return account
    else:
        return Account(
            activeCard=activeCard,
            availableLimit=availableLimit,
            violations=["account-already-initialized"]
        )

def find_account(store, account):
    return find(store, account)
