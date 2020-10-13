from authorizer.application.usecases.transactions.transaction_interface import TransactionInterface
from authorizer.domain.account import Account
from authorizer.domain.transaction import Transaction
from authorizer.application.exceptions import HighFrequencySmallIntervalException

from datetime import datetime


class HighFrequencySmallInterval(TransactionInterface):
    TIME_TOKEN = "%Y-%m-%dT%H:%M:%S.%f%z"

    def minutes(self, delta: datetime):
        return delta.seconds/60

    def is_doubled(self, last_transaction: Transaction, current_transaction: Transaction):
        last_time = datetime.strptime(last_transaction.time, self.TIME_TOKEN)
        curr_time = datetime.strptime(current_transaction.time, self.TIME_TOKEN)
        delta = curr_time - last_time

        return bool(self.minutes(delta) <= 2) if (delta.days <= 0) else False

    def is_same_transaction(current_transaction, another_transaction):
        return bool((current_transaction.merchant) and ())
        pass

    def execute(
        self,
        account_repository,
        transaction_repository,
        transaction_dto
    ):
        transaction = Transaction(**transaction_dto)
        account = account_repository.find()
        transactions = transaction_repository.find()
        if(len(transactions) > 0):
            last_transaction = transactions[-1]

            if((transaction.merchant == last_transaction.merchant) and (transaction.amount == last_transaction.amount)):
                if(self.is_doubled(last_transaction, transaction)):
                    account.violations = ["doubled-transaction"]
            account_repository.save(account)
            raise HighFrequencySmallIntervalException("doubled-transaction")
