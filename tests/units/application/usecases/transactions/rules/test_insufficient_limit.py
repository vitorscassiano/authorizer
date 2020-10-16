from unittest import TestCase, skip
from unittest.mock import Mock, MagicMock

from authorizer.application.usecases.transactions.transaction_manager import TransactionManager
from authorizer.application.usecases.transactions.rules import InsufficientLimitTransaction
from authorizer.domain.account import Account


class TestInsufficientLimit(TestCase):
    def setUp(self):
        self.mock_account_repo = Mock()
        self.mock_transaction_repo = Mock()
        self.transaction_manager = TransactionManager(
            self.mock_account_repo,
            self.mock_transaction_repo
        )
        self.transaction_manager.subscribe(InsufficientLimitTransaction())

    def test_verify_no_insufficient_limit(self):
        mock_transaction = {"amount": 90}
        mock_account = Account(availableLimit=100)
        self.mock_account_repo.find = Mock(return_value=mock_account)

        account = self.transaction_manager.notify(mock_transaction)

        self.assertEqual(account.availableLimit, 10)
        self.mock_account_repo.find.assert_called_once()
        self.mock_account_repo.save.assert_called_once_with(account)

    def test_verify_insufficient_limit(self):
        mock_transaction_dto = {"amount": 90}
        mock_account = Account(availableLimit=10)

        self.mock_account_repo.find = Mock(return_value=mock_account)

        account = self.transaction_manager.notify(mock_transaction_dto)

        self.assertEqual(account.availableLimit, 10)
        self.assertEqual(account.violations, ["insufficient-limit"])
        self.mock_account_repo.find.assert_called_once()
        self.mock_account_repo.save.assert_not_called()
