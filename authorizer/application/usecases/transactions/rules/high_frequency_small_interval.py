from typing import List
from datetime import datetime
from authorizer.domain.account import Account
from authorizer.domain.transaction import Transaction

from authorizer.application.usecases.transactions.transaction_interface import TransactionInterface
from authorizer.domain.account import Account
from authorizer.domain.transaction import Transaction
from authorizer.application.exceptions import HighFrequencySmallIntervalException


class HighFrequencySmallInterval(TransactionInterface):
    TIME_TOKEN = "%Y-%m-%dT%H:%M:%S.%f%z"
    FREQUENCY = 3

    def minutes(self, delta: datetime) -> int:
        return delta.seconds/60

    def get_delta(self, current: Transaction, other: Transaction) -> datetime:
        curr_time = datetime.strptime(current.time, self.TIME_TOKEN)
        last_time = datetime.strptime(other.time, self.TIME_TOKEN)
        return curr_time - last_time

    def filter_interval(
        self,
        current_transaction: Transaction,
        transactions: List[Transaction],
        interval=2
    ) -> List:
        return list(
            filter(
                lambda time: self.minutes(time) <= interval,
                map(
                    lambda t: self.get_delta(current_transaction, t),
                    transactions
                )
            )
        )

    def execute(
        self,
        account_repo,
        transaction_repo,
        account: Account,
        transaction: Transaction
    ) -> None:
        transactions = transaction_repo.find_all()
        high_frequency = self.filter_interval(transaction,transactions)

        if(len(high_frequency) >= self.FREQUENCY):
            raise HighFrequencySmallIntervalException("high-frequency-small-interval")
