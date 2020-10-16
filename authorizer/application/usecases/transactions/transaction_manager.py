from authorizer.application.repositories.storage import Storage
from authorizer.application.usecases.account import AccountUsecase
from authorizer.domain.account import Account
from authorizer.domain.transaction import Transaction
from authorizer.application.exceptions import (
    CardNotActiveException,
    DoubledException,
    InsufficientLimitException,
    HighFrequencySmallIntervalException,
)


def withdraw(lessening, subtrahend):
    return lessening - subtrahend

class TransactionManager():
    def __init__(self, account_repo, transaction_repo):
        self.subscriptions = []
        self.account_repo = account_repo
        self.transaction_repo = transaction_repo

    def subscribe(self, *transactions) -> None:
        for transaction in transactions:
            self.subscriptions.append(transaction)

    def unsubscribe(self, *transactions) -> None:
        for transaction in transactions:
            self.subscriptions.remove(transaction)

    def notify(self, transaction_dto: dict) -> Account:
        account = self.account_repo.find()
        transaction = Transaction(**transaction_dto)
        try:
            for subscription in self.subscriptions:
                subscription.execute(
                    self.account_repo,
                    self.transaction_repo,
                    account,
                    transaction
                )
            self.transaction_repo.save(transaction)

            new_limit = withdraw(account.availableLimit, transaction.amount)
            new_account = Account(
                activeCard=account.activeCard,
                availableLimit=new_limit
            )
            self.account_repo.save(new_account)
            return new_account
        except (
            CardNotActiveException,
            DoubledException,
            InsufficientLimitException,
            HighFrequencySmallIntervalException
        ) as e:
            return Account(
                activeCard=account.activeCard,
                availableLimit=account.availableLimit,
                violations=[str(e)]
            )
        except Exception as e:
            print(e)
            raise e
