from typing import List
from datetime import datetime, timedelta
from authorizer.domain.account import Account
from authorizer.domain.transaction import Transaction
from authorizer.application.usecases.transactions.transaction_interface import TransactionInterface
from authorizer.application.exceptions import HighFrequencySmallIntervalException

FREQUENCY = 3
TIMETOKEN="%Y-%m-%dT%H:%M:%S.%f%z"


def minutes(delta: datetime) -> int:
    return delta.seconds/60

def p_time(time: str):
    return datetime.strptime(time, TIMETOKEN)

def filter_interval(
    transaction: Transaction,
    transactions: List[Transaction],
    INTERVAL=2
) -> List:
    delta = timedelta(minutes=INTERVAL)
    current_time = p_time(transaction.time)
    start = current_time - delta

    return filter(
        lambda t: p_time(t.time) >= start and p_time(t.time) <= current_time,
        transactions
    )

class HighFrequencyPolicy(TransactionInterface):
    @staticmethod
    def execute(repository, account: Account, transaction: Transaction):
        transactions = repository.find_all_transactions()
        high_frequency = filter_interval(transaction, transactions)

        if(len(list(high_frequency)) >= FREQUENCY):
            raise HighFrequencySmallIntervalException(
                "high-frequency-small-interval")
