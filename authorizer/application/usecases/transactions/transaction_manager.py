from authorizer.domain.account import Account
from authorizer.domain.transaction import Transaction
from authorizer.application.exceptions import (
    CardNotActiveException,
    DoubledException,
    InsufficientLimitException,
    HighFrequencySmallIntervalException,
)


def subtract(lessening, subtrahend):
    return lessening - subtrahend


def make_transaction(repository, account, transaction):
    new_limit = subtract(account.availableLimit, transaction.amount)
    new_account = Account(
        activeCard=account.activeCard,
        availableLimit=new_limit
    )
    repository.save_account(new_account)
    return new_account


def policies():
    return (
        CardNotActiveException,
        DoubledException,
        InsufficientLimitException,
        HighFrequencySmallIntervalException
    )


class TransactionManager():
    def __init__(self, repository):
        self.subscriptions = []
        self.repository = repository

    def subscribe(self, *transactions) -> None:
        for transaction in transactions:
            self.subscriptions.append(transaction)

    def unsubscribe(self, *transactions) -> None:
        for transaction in transactions:
            self.subscriptions.remove(transaction)

    def process(self, transaction_dto: dict) -> Account:
        account = self.repository.find_account()
        transaction = Transaction(**transaction_dto)
        try:
            # breakpoint()
            for subscription in self.subscriptions:
                subscription.execute(self.repository, account, transaction)
            self.repository.save_transaction(transaction)

            processed = make_transaction(self.repository, account, transaction)
            return processed
        except policies() as e:
            return Account(
                activeCard=account.activeCard,
                availableLimit=account.availableLimit,
                violations=[str(e)]
            )
        except Exception as e:
            raise e
