from typing import List
from datetime import datetime
from authorizer.domain.account import Account
from authorizer.domain.transaction import Transaction
from authorizer.application.usecases.transactions.transaction_interface import TransactionInterface
from authorizer.application.exceptions import HighFrequencySmallIntervalException

FREQUENCY = 3


def minutes(delta: datetime) -> int:
    return delta.seconds/60


def get_delta(current: str, other: str, TIMETOKEN="%Y-%m-%dT%H:%M:%S.%f%z") -> datetime:
    curr_time = datetime.strptime(current, TIMETOKEN)
    last_time = datetime.strptime(other, TIMETOKEN)
    return curr_time - last_time


def filter_interval(transaction: Transaction, transactions: List[Transaction], INTERVAL=2) -> List:
    return filter(
        lambda time: minutes(time) <= INTERVAL,
        map(lambda t: get_delta(transaction.time, t.time), transactions)
    )


class HighFrequencyPolicy(TransactionInterface):
    @staticmethod
    def execute(repository, account: Account, transaction: Transaction):
        transactions = repository.find_all_transactions()
        high_frequency = filter_interval(transaction, transactions)

        if(len(list(high_frequency)) >= FREQUENCY):
            raise HighFrequencySmallIntervalException(
                "high-frequency-small-interval")
