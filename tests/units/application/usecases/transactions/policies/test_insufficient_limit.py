from unittest.mock import Mock
from authorizer.domain.account import Account
from authorizer.application.usecases.transactions.transaction_manager \
    import TransactionManager
from authorizer.application.usecases.transactions.policies \
    import InsufficientLimitPolicy


def test_should_be_insufficient_limit():
    repository = Mock()
    repository.find_account.return_value = Account()
    manager = TransactionManager(repository)
    manager.subscribe(InsufficientLimitPolicy)
    transaction_dto = dict(amount=90)

    expected_account = Account(violations=["insufficient-limit"])

    processed_account = manager.process(transaction_dto)

    repository.find_account.assert_called_once()
    assert processed_account == expected_account


def test_should_be_no_insufficient_limit():
    repository = Mock()
    repository.find_account.return_value = Account(availableLimit=90)
    manager = TransactionManager(repository)
    manager.subscribe(InsufficientLimitPolicy)
    transaction_dto = dict(amount=10)
    expected_account = Account(availableLimit=80, violations=[])

    processed_account = manager.process(transaction_dto)

    repository.find_account.assert_called_once()
    assert processed_account == expected_account
