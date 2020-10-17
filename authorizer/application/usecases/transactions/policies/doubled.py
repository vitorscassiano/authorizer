from datetime import datetime

from authorizer.application.usecases.transactions.transaction_interface import TransactionInterface
from authorizer.domain.account import Account
from authorizer.domain.transaction import Transaction
from authorizer.application.exceptions import DoubledException


def minutes(delta: datetime):
    return delta.seconds/60


def is_double(
    current: str,
    other: str,
    TIMETOKEN="%Y-%m-%dT%H:%M:%S.%f%z",
    INTERVAL=2
):
    current_time = datetime.strptime(current, TIMETOKEN)
    other_time = datetime.strptime(other, TIMETOKEN)
    delta = current_time - other_time

    return bool(minutes(delta) <= INTERVAL) if delta.days <= 0 else False


def filter_doubles(transaction, transactions):
    return filter(
        lambda t: t == transaction,
        filter(
            lambda t: is_double(transaction.time, t.time) == True,
            transactions
        )
    )


class DoubledPolicy(TransactionInterface):
    @staticmethod
    def execute(repository, account, transaction):
        transactions = repository.find_all_transactions()
        doubles = filter_doubles(transaction, transactions)
        if(len(list(doubles)) >= 1):
            raise DoubledException("doubled-transaction")
