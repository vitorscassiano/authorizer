from authorizer.application.usecases.transactions.transaction_interface import TransactionInterface
from authorizer.domain.account import Account
from authorizer.domain.transaction import Transaction
from authorizer.application.exceptions import DoubledException

from datetime import datetime


class DoubledTransaction(TransactionInterface):
    TIME_TOKEN = "%Y-%m-%dT%H:%M:%S.%f%z"

    def minutes(self, delta: datetime):
        return delta.seconds/60

    def is_doubled(self, transaction: Transaction, other: Transaction):
        current_time = datetime.strptime(transaction.time, self.TIME_TOKEN)
        last_time = datetime.strptime(other.time, self.TIME_TOKEN)
        delta = current_time - last_time

        if(delta.days <= 0):
            return bool(self.minutes(delta) <= 2)
        else:
            False

    def execute(self, account_repo, transaction_repo, account, transaction):
        transactions = transaction_repo.find_all()
        if(len(transactions) > 0):
            last_transaction = transactions[-1]

            if(transaction == last_transaction):
                if(self.is_doubled(transaction, last_transaction)):
                    raise DoubledException("doubled-transaction")
