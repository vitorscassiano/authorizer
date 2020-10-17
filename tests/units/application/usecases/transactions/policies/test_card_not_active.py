import pytest
from unittest.mock import Mock
from authorizer.domain.account import Account
from authorizer.application.usecases.transactions.transaction_manager import TransactionManager
from authorizer.application.usecases.transactions.policies import CardNotActivePolicy


def test_should_verify_card_not_active():
    repository = Mock()
    repository.find_account.return_value = Account(False)
    manager = TransactionManager(repository)
    manager.subscribe(CardNotActivePolicy)
    transaction_dto = {}

    expected_account = Account(False, violations=["card-not-active"])

    processed_account = manager.process(transaction_dto)

    repository.find_account.assert_called_once()
    assert processed_account == expected_account

def test_should_verify_account_not_found():
    repository = Mock()
    repository.find_account.return_value = None
    manager = TransactionManager(repository)
    manager.subscribe(CardNotActivePolicy)
    transaction_dto = {}

    expected_account = Account()

    with pytest.raises(Exception) as execinfo:
        manager.process(transaction_dto)

    repository.find_account.assert_called_once()
    assert "account-not-found" in str(execinfo.value)
