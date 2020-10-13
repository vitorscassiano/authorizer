from unittest import TestCase
from unittest.mock import Mock
from authorizer.application.usecases.account import AccountUsecase
from authorizer.domain.account import Account


class TestAccount(TestCase):
  def setUp(self):
    self.mock_repository = Mock()
    self.account_usecase = AccountUsecase(self.mock_repository)

  def test_should_create_account(self):
    self.mock_repository.is_empty.return_value = True
    self.account_usecase.create(active_card=True, available_limit=100)

    self.mock_repository.is_empty.assert_called_once()
    self.mock_repository.find.assert_not_called()
    self.mock_repository.save.assert_called_once()

  def test_should_raise_account_already_initialized(self):
    self.mock_repository.is_empty.return_value = False
    mock_account = Mock()
    mock_account.violations = []
    self.mock_repository.find.return_value = mock_account

    self.account_usecase.create(True, 100)

    self.mock_repository.is_empty.assert_called_once()
    self.mock_repository.find.assert_called_once()
    self.mock_repository.save.assert_called_once()
    self.assertListEqual(mock_account.violations, ["account-already-initialized"])