from authorizer.application.repositories.storage import Storage
from authorizer.application.usecases.account import AccountUsecase
from authorizer.domain.transaction import Transaction
from authorizer.application.exceptions import (
    CardNotActiveException,
    DoubledException,
    SubtractBalanceException,
    HighFrequencySmallIntervalException,
)


class TransactionManager():
    def __init__(self, account_repo, transaction_repo):
        self.subscriptions = []
        self.account_repo = account_repo
        self.transaction_repo = transaction_repo

    def subscribe(self, *transactions):
        for transaction in transactions:
            self.subscriptions.append(transaction)

    def unsubscribe(self, *transactions):
        for transaction in transactions:
            self.subscriptions.remove(transaction)

    def notify(self, transaction_dto: dict):
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
            account = self.account_repo.find() # account.id
            return account
        except (
            CardNotActiveException,
            DoubledException,
            SubtractBalanceException,
            HighFrequencySmallIntervalException
        ) as e:
            account.violations = [str(e)]
            return account
        except Exception as e:
            print(e)
