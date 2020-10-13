from unittest import TestCase, skip
from unittest.mock import Mock, MagicMock
from tests.helpers.assert_any_helper import Any

from authorizer.application.usecases.transactions.transaction_manager import TransactionManager
from authorizer.application.usecases.transactions.rules import SubtractBalanceTransaction
from authorizer.domain.account import Account


class TestSubtractBalance(TestCase):
  def setUp(self):
    self.mock_account_repo = Mock()
    self.mock_transaction_repo = Mock()
    self.transaction_manager = TransactionManager(
      self.mock_account_repo,
      self.mock_transaction_repo
    )
    self.transaction_manager.subscribe(SubtractBalanceTransaction())

  def test_verify_subtract_from_balance(self):
    mock_transaction_dto = {"amount": 90}
    mock_account = Mock()
    mock_account.availableLimit = 100

    self.mock_account_repo.find.return_value = mock_account

    self.transaction_manager.notify(mock_transaction_dto)

    self.assertEqual(mock_account.availableLimit, 10)
    self.mock_account_repo.save.assert_called_once()

  def test_verify_insufficient_limit(self):
    mock_transaction_dto = {"amount": 90}
    mock_account = Mock()
    mock_account.availableLimit = 10
    mock_account.violations = []

    self.mock_account_repo.find.return_value = mock_account

    self.transaction_manager.notify(mock_transaction_dto)

    self.assertEqual(mock_account.availableLimit, 10)
    self.assertEqual(mock_account.violations, ["insufficient-limit"])
    self.mock_account_repo.save.assert_called_once()
