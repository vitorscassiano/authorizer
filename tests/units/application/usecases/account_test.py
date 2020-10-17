from unittest.mock import Mock
from authorizer.application.usecases.account import AccountUsecase
from authorizer.domain.account import Account


def test_should_be_created_account():
    mock_repository = Mock()
    mock_repository.is_account_empty.return_value = True
    account_usecase = AccountUsecase(mock_repository)
    account = account_usecase.create(True, available_limit=0)
    expected_account = Account()

    mock_repository.is_account_empty.assert_called_once()
    mock_repository.save_account.assert_called_once()
    assert account == expected_account

def test_should_not_be_created_account():
    mock_repository = Mock()
    mock_repository.is_account_empty.return_value = False
    account_usecase = AccountUsecase(mock_repository)

    account = account_usecase.create(True, 0)
    expected_account = Account(violations=["account-already-initialized"])

    mock_repository.is_account_empty.assert_called_once()
    mock_repository.save_account.assert_not_called()
    assert account == expected_account
