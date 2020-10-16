from unittest import TestCase
from unittest.mock import Mock, MagicMock

from authorizer.application.usecases.transactions.transaction_manager import TransactionManager
from authorizer.application.usecases.transactions.rules import HighFrequencySmallInterval
from authorizer.domain.account import Account
from authorizer.domain.transaction import Transaction
from authorizer.application.repositories import (
    AccountRepository,
    TransactionRepository
)


class TestHighFrequencySmallInteval(TestCase):
    def setUp(self):
        self.mock_account_repo = AccountRepository()
        self.mock_transaction_repo = TransactionRepository()
        self.transaction_manager = TransactionManager(
            self.mock_account_repo,
            self.mock_transaction_repo
        )
        self.high_frequency = HighFrequencySmallInterval()
        self.transaction_manager.subscribe(self.high_frequency)

    def test_should_get_delta_time(self):
        transaction_a = Transaction(time="2019-02-13T10:10:00.000Z")
        transaction_b = Transaction(time="2019-02-13T10:00:00.000Z")
        delta = self.high_frequency.get_delta(transaction_a, transaction_b)
        self.assertEqual(delta.seconds, 600)

    def test_should_filter_frequency(self):
        transaction = Transaction(time="2019-02-13T10:05:00.000Z")
        transactions = [
            Transaction(time="2019-02-13T10:00:00.000Z"),
            Transaction(time="2019-02-13T10:01:00.000Z"),
            Transaction(time="2019-02-13T10:02:00.000Z"),
            Transaction(time="2019-02-13T10:03:00.000Z"),
            Transaction(time="2019-02-13T10:04:00.000Z"),
        ]

        filtered = self.high_frequency.filter_interval(
            transaction,
            transactions
        )

        self.assertEquals(len(filtered), 2)

    def test_should_verify_frequency_of_transactions(self):
        mock_account = Account(True, 100)
        mock_transaction = {"merchant": "Burguer King", "amount": 10}

        self.mock_account_repo.find = Mock(return_value=mock_account)

        mock_transaction["time"] = "2019-02-13T10:00:00.000Z"
        self.transaction_manager.notify(mock_transaction)

        mock_transaction["time"] = "2019-02-13T10:00:30.000Z"
        self.transaction_manager.notify(mock_transaction)

        mock_transaction["time"] = "2019-02-13T10:01:00.000Z"
        self.transaction_manager.notify(mock_transaction)

        mock_transaction["time"] = "2019-02-13T10:01:30.000Z"
        account = self.transaction_manager.notify(mock_transaction)

        self.assertListEqual(
            account.violations,
            ["high-frequency-small-interval"]
        )
