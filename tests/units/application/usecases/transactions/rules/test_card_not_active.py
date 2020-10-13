from unittest import TestCase, skip
from unittest.mock import Mock, MagicMock
from tests.helpers.assert_any_helper import Any

from authorizer.application.usecases.transactions.transaction_manager import TransactionManager
from authorizer.application.usecases.transactions.rules import CardNotActiveTransaction
from authorizer.domain.account import Account


class TestCardNotActiveTransactionn(TestCase):
  def setUp(self):
    self.mock_account_repo = Mock()
    self.mock_transaction_repo = Mock()
    self.transaction_manager = TransactionManager(
      self.mock_account_repo,
      self.mock_transaction_repo
    )
    self.transaction_manager.subscribe(CardNotActiveTransaction())

  def test_should_verify_card_is_not_active(self):
    mock_account = Mock()
    mock_account.violations = []
    self.mock_account_repo.find.return_value = mock_account
    mock_account.active_card = False
    mock_transaction = {}

    self.transaction_manager.notify(mock_transaction)

    self.mock_account_repo.find.assert_called_once()
    self.assertListEqual(mock_account.violations, ["card-not-active"])

  @skip("does not implemented")
  def test_should_verify_account_not_found(self):
    mock_account = Mock()
    self.mock_account_repository.find.return_value = False
    mock_transaction = Mock()

    with self.assertRaises(Exception) as e:
      self.transaction_manager.notify(mock_account, mock_transaction)

    self.mock_account_repo.find.assert_called_once()
    self.assertListEqual(str(e), ["card-not-active"])
