from unittest import TestCase, skip
from unittest.mock import Mock, MagicMock
from tests.helpers.assert_any_helper import Any

from authorizer.application.usecases.transactions.transaction_manager import TransactionManager
from authorizer.application.usecases.transactions.rules import HighFrequencySmallInterval
from authorizer.domain.account import Account


class TestHighFrequencySmallInteval(TestCase):
  def setUp(self):
    self.transaction_manager = TransactionManager()
    self.transaction_manager.subscribe(HighFrequencySmallInterval())

  @skip("does not implemented")
  def test_should_verify_card_is_not_active(self):
    mock_account = MagicMock()
    mock_account.active_card = False

    mock_repository = Mock()
    mock_repository.find.return_value = mock_account

    mock_transaction = Mock()

    self.transaction_manager.notify(mock_repository, mock_account, mock_transaction)
    self.transaction_manager.notify(mock_repository, mock_account, mock_transaction)

    # mock_repository.find.assert_called_once_with(Any(Account))
    # self.assertListEqual(mock_account.violations, ["card-not-active"])
