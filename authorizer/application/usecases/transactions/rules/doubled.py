from authorizer.application.usecases.transactions.transaction_interface import TransactionInterface
from authorizer.domain.account import Account
from authorizer.domain.transaction import Transaction
from authorizer.application.exceptions import DoubledException

from datetime import datetime


class DoubledTransaction(TransactionInterface):
    TIME_TOKEN = "%Y-%m-%dT%H:%M:%S.%f%z"
    MINUTES_INTERVAL = 2

    def minutes(self, delta: datetime):
        return delta.seconds/60

    def is_doubled(self, current: Transaction, other: Transaction):
        current_time = datetime.strptime(current.time, self.TIME_TOKEN)
        other_time = datetime.strptime(other.time, self.TIME_TOKEN)
        delta = current_time - other_time

        if(delta.days <= 0):
            return bool(self.minutes(delta) <= self.MINUTES_INTERVAL)
        else:
            False

    def filter_doubled(self, transaction, transactions):
        return list(
            filter(
                lambda t: t==transaction,
                filter(
                    lambda t: self.is_doubled(transaction, t) == True,
                    transactions
                )
            )
        )

    def execute(self, account_repo, transaction_repo, account, transaction):
        transactions = transaction_repo.find_all()
        if(len(self.filter_doubled(transaction, transactions)) >= 1):
            raise DoubledException("doubled-transaction")
