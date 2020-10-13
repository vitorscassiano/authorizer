from unittest import TestCase, skip
from unittest.mock import Mock, MagicMock

from authorizer.application.usecases.transactions.transaction_manager import (
    TransactionManager
)
from authorizer.application.usecases.transactions.rules import (
    CardNotActiveTransaction
)
from authorizer.application.repositories import AccountRepository
from authorizer.domain.account import Account


class TestCardNotActiveTransactionn(TestCase):
    def setUp(self):
        self.mock_account_repo = AccountRepository()
        self.mock_transaction_repo = Mock()
        self.transaction_manager = TransactionManager(
            self.mock_account_repo,
            self.mock_transaction_repo
        )
        self.transaction_manager.subscribe(CardNotActiveTransaction())

    def test_should_verify_card_is_not_active(self):
        mock_account = {"activeCard": False}
        mock_transaction = {}
        self.mock_account_repo.find = Mock(return_value=Account(**mock_account))

        account = self.transaction_manager.notify(mock_transaction)

        self.mock_account_repo.find.assert_called_once()
        self.assertListEqual(account.violations, ["card-not-active"])

    @skip("does not implemented")
    def test_should_verify_account_not_found(self):
        mock_account = {}
        mock_transaction = {}
        self.mock_account_repository.find.return_value = False

        with self.assertRaises(Exception) as e:
            self.transaction_manager.notify(mock_account, mock_transaction)

        self.mock_account_repo.find.assert_called_once()
        self.assertListEqual(str(e), ["card-not-active"])
