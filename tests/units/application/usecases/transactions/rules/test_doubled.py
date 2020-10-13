from unittest import TestCase, skip
from unittest.mock import Mock, MagicMock
from tests.helpers.assert_any_helper import Any

from authorizer.application.usecases.transactions.transaction_manager import TransactionManager
from authorizer.application.usecases.transactions.rules import DoubledTransaction
from authorizer.domain.account import Account
from authorizer.domain.transaction import Transaction
from authorizer.application.repositories import (
    AccountRepository,
    TransactionRepository
)


class TestDoubledTransaction(TestCase):
    def setUp(self):
        self.mock_account_repo = AccountRepository()
        self.mock_transaction_repo = TransactionRepository()
        self.transaction_manager = TransactionManager(
            self.mock_account_repo,
            self.mock_transaction_repo
        )
        self.doubled_transaction = DoubledTransaction()
        self.transaction_manager.subscribe(self.doubled_transaction)

    def test_is_doubled(self):
        current_transaction = Transaction(time="2019-02-13T10:00:00.000Z")
        last_transaction = Transaction(time="2019-02-13T10:00:00.000Z")
        is_doubled = self.doubled_transaction.is_doubled(
            current_transaction,
            last_transaction
        )
        self.assertTrue(is_doubled)

        current_transaction = Transaction(time="2019-02-13T10:01:59.000Z")
        last_transaction = Transaction(time="2019-02-13T10:00:00.000Z")
        is_doubled = self.doubled_transaction.is_doubled(
            current_transaction,
            last_transaction
        )
        self.assertTrue(is_doubled)

        current_transaction = Transaction(time="2019-02-13T10:02:01.000Z")
        last_transaction = Transaction(time="2019-02-13T10:00:00.000Z")
        is_doubled = self.doubled_transaction.is_doubled(
            current_transaction,
            last_transaction
        )
        self.assertFalse(is_doubled)

        current_transaction = Transaction(time="2019-02-13T10:03:00.000Z")
        last_transaction = Transaction(time="2019-02-13T10:00:00.000Z")
        is_doubled = self.doubled_transaction.is_doubled(
            current_transaction,
            last_transaction
        )
        self.assertFalse(is_doubled)

        current_transaction = Transaction(time="2019-02-14T10:03:00.000Z")
        last_transaction = Transaction(time="2019-02-13T10:00:00.000Z")
        is_doubled = self.doubled_transaction.is_doubled(
            current_transaction,
            last_transaction
        )
        self.assertFalse(is_doubled)


    def test_should_verify_no_doubled_transaction(self):
        mock_account_dto = {}
        mock_transaction_dto = {"merchant": "Burguer King", "amount": 10}
        self.mock_transaction_repo.find_all = Mock(return_value=[
            Transaction(
                **mock_transaction_dto,
                time="2019-02-13T10:00:00.000Z"
            )
        ])

        mock_account = Mock()
        mock_account.violations = []
        self.mock_account_repo.find = Mock(return_value=mock_account)
        mock_transaction_dto["time"] = "2019-02-14T10:00:00.000Z"

        account = self.transaction_manager.notify(mock_transaction_dto)

        self.mock_transaction_repo.find_all.assert_called_once()
        self.assertEqual(self.mock_account_repo.find.call_count, 2)
        self.assertListEqual(account.violations, [])

    def test_should_verify_doubled_transaction(self):
        mock_transaction_dto = {
            "merchant": "Burguer King",
            "amount": 10,
            "time": "2019-02-14T10:00:00.000Z"
        }
        mock_account_dto = {}
        mock_account = Mock()
        mock_account.violations = []
        self.mock_account_repo.find = Mock(return_value=mock_account)
        self.mock_transaction_repo.find_all = Mock(return_value=[
            Transaction(**mock_transaction_dto)
        ])

        account = self.transaction_manager.notify(mock_transaction_dto)

        self.mock_transaction_repo.find_all.assert_called_once()
        self.mock_account_repo.find.assert_called_once()
        self.assertListEqual(account.violations, ["doubled-transaction"])
