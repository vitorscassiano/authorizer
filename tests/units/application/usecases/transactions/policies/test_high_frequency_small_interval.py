from unittest.mock import Mock
from authorizer.domain.account import Account
from authorizer.domain.transaction import Transaction

from authorizer.application.usecases.transactions.transaction_manager import TransactionManager
from authorizer.application.usecases.transactions.policies import HighFrequencyPolicy
from authorizer.application.usecases.transactions.policies.high_frequency_small_interval import get_delta, filter_interval


def test_should_be_got_delta():
    time_a = "2019-02-13T10:10:00.000Z"
    time_b = "2019-02-13T10:00:00.000Z"
    delta = get_delta(time_a, time_b)

    assert delta.seconds == 600


def test_should_be_filtered_frequency():
    transaction = Transaction(time="2019-02-13T10:05:00.000Z")
    transactions = [
        Transaction(time="2019-02-13T10:00:00.000Z"),
        Transaction(time="2019-02-13T10:01:00.000Z"),
        Transaction(time="2019-02-13T10:02:00.000Z"),
        Transaction(time="2019-02-13T10:03:00.000Z"),
        Transaction(time="2019-02-13T10:04:00.000Z"),
    ]

    intervals = filter_interval(transaction, transactions)

    assert len(list(intervals)) == 2


def test_should_be_verified_frequency_transactions_v1():
    transaction_dto = dict(time="2019-02-13T10:01:30.000Z")
    repository = Mock()
    repository.find_account.return_value = Account()
    repository.find_all_transactions.return_value = [
        Transaction(time="2019-02-13T10:00:00.000Z"),
        Transaction(time="2019-02-13T10:00:30.000Z"),
        Transaction(time="2019-02-13T10:01:00.000Z"),
    ]
    manager = TransactionManager(repository)
    manager.subscribe(HighFrequencyPolicy)

    processed_account = manager.process(transaction_dto)

    expected_account = Account(violations=["high-frequency-small-interval"])

    repository.find_account.assert_called_once()
    repository.find_all_transactions.assert_called_once()
    assert processed_account == expected_account


def test_should_be_verified_frequency_transactions_v2():
    db = []
    transaction_dto = dict(time="2019-02-13T10:00:00.000Z")
    repository = Mock()
    repository.find_account.return_value = Account()
    repository.find_all_transactions.return_value = db
    repository.save_transaction = Mock()
    manager = TransactionManager(repository)
    manager.subscribe(HighFrequencyPolicy)

    manager.process(transaction_dto)

    transaction_dto = dict(time="2019-02-13T10:00:30.000Z")
    db = db + [Transaction(**transaction_dto)]
    repository.find_all_transactions.return_value = db

    manager.process(transaction_dto)

    transaction_dto = dict(time="2019-02-13T10:01:00.000Z")
    db = db + [Transaction(**transaction_dto)]
    repository.find_all_transactions.return_value = db
    manager.process(transaction_dto)

    transaction_dto = dict(time="2019-02-13T10:01:30.000Z")
    db = db + [Transaction(**transaction_dto)]
    repository.find_all_transactions.return_value = db
    processed_account = manager.process(transaction_dto)

    expected_account = Account(violations=["high-frequency-small-interval"])

    assert repository.find_account.call_count == 4
    assert repository.save_transaction.call_count == 3
    assert repository.find_all_transactions.call_count == 4
    assert processed_account == expected_account
