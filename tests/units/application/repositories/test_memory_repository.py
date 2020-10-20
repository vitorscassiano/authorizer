import pytest
from unittest.mock import Mock

from authorizer.application.repositories.memory_repository \
    import MemoryRepository, ACCOUNTS, TRANSACTIONS


@pytest.fixture(scope="session")
def repository():
    return MemoryRepository()


def test_should_get_none_account(repository):
    response = repository.find_account()

    assert not response


def test_should_get_account(repository):
    mock_account = Mock()
    repository.storage[ACCOUNTS] = [mock_account]

    response = repository.find_account()

    assert response == mock_account


def test_should_save_account(repository):
    mock_account = Mock()
    repository.save_account(mock_account)

    assert len(repository.storage[ACCOUNTS]) == 1
    assert len(repository.storage[TRANSACTIONS]) == 0


def test_should_save_transaction(repository):
    repository.clean()
    mock_transaction = Mock()
    repository.save_transaction(mock_transaction)

    assert len(repository.storage[TRANSACTIONS]) == 1
    assert len(repository.storage[ACCOUNTS]) == 0


def test_should_get_all_transactions(repository):
    repository.clean()
    mock_transaction = Mock()
    repository.storage[TRANSACTIONS] = [mock_transaction for i in range(5)]

    transactions = repository.all_transactions()

    assert len(transactions) == 5
