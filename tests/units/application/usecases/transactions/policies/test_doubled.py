from unittest.mock import Mock
from authorizer.domain.account import Account
from authorizer.domain.transaction import Transaction
from authorizer.application.usecases.transactions.transaction_manager import TransactionManager
from authorizer.application.usecases.transactions.policies.doubled import DoubledPolicy, is_double, filter_doubles


def test_should_be_double():
    d = is_double("2019-02-13T10:00:00.000Z", "2019-02-13T10:00:00.000Z")
    assert d == True

    d = is_double("2019-02-13T10:01:59.000Z", "2019-02-13T10:00:00.000Z")
    assert d == True

    d = is_double("2019-02-13T10:02:01.000Z", "2019-02-13T10:00:00.000Z")
    assert d == False

    d = is_double("2019-02-13T10:03:00.000Z", "2019-02-13T10:00:00.000Z")
    assert d == False

    d = is_double("2019-02-14T10:03:00.000Z", "2019-02-13T10:00:00.000Z")
    assert d == False


def test_should_be_filtered_doubles():
    transaction = Transaction(time="2019-02-13T10:03:00.000Z")
    transactions = [
        Transaction(time="2019-02-13T10:00:00.000Z"),
        Transaction(time="2019-02-13T10:02:01.000Z"),
        Transaction(time="2019-02-13T10:01:59.000Z"),
    ]
    doubles = filter_doubles(transaction, transactions)

    assert len(list(doubles)) == 2


def test_should_be_no_doubled_transaction():
    transaction_dto = dict(time="2019-02-13T10:06:03.000Z")
    repository = Mock()
    repository.find_account.return_value = Account()
    repository.all_transactions.return_value = [
        Transaction(time="2019-02-13T10:00:00.000Z"),
        Transaction(time="2019-02-13T10:02:01.000Z"),
        Transaction(time="2019-02-13T10:04:02.000Z"),
    ]
    manager = TransactionManager(repository)
    manager.subscribe(DoubledPolicy())
    processed_account = manager.process(transaction_dto)
    expected_account = Account()

    repository.find_account.assert_called_once()
    repository.all_transactions.assert_called_once()
    assert processed_account == expected_account


def test_should_be_doubled_transactionsn():
    transaction_dto = dict(time="2019-02-13T10:01:30.000Z")

    repository = Mock()
    repository.find_account.return_value = Account()
    repository.all_transactions.return_value = [
        Transaction(time="2019-02-13T10:00:00.000Z"),
        Transaction(time="2019-02-13T10:00:30.000Z"),
        Transaction(time="2019-02-13T10:10:00.000Z"),
    ]
    manager = TransactionManager(repository)
    manager.subscribe(DoubledPolicy)

    processed_account = manager.process(transaction_dto)

    expected_account = Account(violations=["doubled-transaction"])

    assert processed_account == expected_account
