from typing import List
from functools import reduce
from authorizer.domain.account import Account
from authorizer.domain.transaction import Transaction
from authorizer.application.repositories import MemoryRepository


def subtract(lessening: int, subtrahend: int) -> int:
    return lessening - subtrahend


def make_transaction(
    repository: MemoryRepository,
    account: Account,
    transaction: Transaction
) -> Account:
    new_limit = subtract(account.availableLimit, transaction.amount)
    new_account = Account(
        activeCard=account.activeCard,
        availableLimit=new_limit
    )
    repository.save_account(new_account)
    return new_account


class TransactionManager():
    def __init__(self, repository):
        self.subscriptions = []
        self.repository = repository

    def subscribe(self, *transactions: List[Transaction]) -> None:
        for transaction in transactions:
            self.subscriptions.append(transaction)

    def unsubscribe(self, *transactions: List[Transaction]) -> None:
        for transaction in transactions:
            self.subscriptions.remove(transaction)

    def process(self, transaction_dto: dict) -> Account:
        transaction = Transaction(**transaction_dto)
        try:
            account = self.repository.find_account()
            if not(account):
                raise Exception("account-not-found")

            violations = reduce(
                lambda c, n: c + n.execute(
                    self.repository,
                    account,
                    transaction
                ),
                self.subscriptions,
                []
            )

            self.repository.save_transaction(transaction)
            if(len(violations) > 0):
                return Account(
                    activeCard=account.activeCard,
                    availableLimit=account.availableLimit,
                    violations=violations
                )

            processed = make_transaction(self.repository, account, transaction)
            return processed
        except Exception as e:
            raise e
