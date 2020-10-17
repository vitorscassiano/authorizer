import pytest
from unittest import skip
from authorizer.application.controllers import create_account_handler, transaction_handler
from authorizer.application.repositories import MemoryRepository
from authorizer.application.usecases import AccountUsecase, TransactionManager
from authorizer.application.usecases.transactions.policies import get_all_policies

@pytest.fixture(scope="session")
def repository():
    return MemoryRepository()

def test_should_verify_insufficient_limit(repository):
    operations = [
        {"account": {"activeCard": True, "availableLimit": 100}},
        {
            "transaction": {
                "merchant": "Burger King",
                "amount": 120,
                "time": "2019-02-13T10:00:00.000Z"
            }
        }
    ]
    repository.clean()

    a_usecase = AccountUsecase(repository)
    t_usecase = TransactionManager(repository)
    t_usecase.subscribe(*get_all_policies())

    create_account_handler(operations[0], a_usecase)
    processed = transaction_handler(operations[1], t_usecase)

    expected = {
        "account": {
            "activeCard": True,
            "availableLimit": 100,
            "violations": ["insufficient-limit"]
        }
    }
    assert processed == expected


def test_should_verify_double_transactions(repository):
    operations = [
        {"account": {"activeCard": True, "availableLimit": 100}},
        {
            "transaction": {
                "merchant": "Burger King",
                "amount": 20,
                "time": "2019-02-13T10:00:00.000Z"
            }
        },
        {
            "transaction": {
                "merchant": "Burger King",
                "amount": 20,
                "time": "2019-02-13T10:01:50.000Z"
            }
        },
    ]
    repository.clean()

    a_usecase = AccountUsecase(repository)
    t_usecase = TransactionManager(repository)
    t_usecase.subscribe(*get_all_policies())

    create_account_handler(operations[0], a_usecase)
    transaction_handler(operations[1], t_usecase)
    processed = transaction_handler(operations[2], t_usecase)

    expected = {
        "account": {
            "activeCard": True,
            "availableLimit": 80,
            "violations": ["doubled-transaction"]
        }
    }
    assert processed == expected


def test_should_verify_no_double_transactions(repository):
    operations = [
        {"account": {"activeCard": True, "availableLimit": 100}},
        {
            "transaction": {
                "merchant": "Burger King",
                "amount": 20,
                "time": "2019-02-13T10:00:00.000Z"
            }
        },
        {
            "transaction": {
                "merchant": "Burger King",
                "amount": 20,
                "time": "2019-02-13T10:02:10.000Z"
            }
        },
    ]
    repository.clean()

    a_usecase = AccountUsecase(repository)
    t_usecase = TransactionManager(repository)
    t_usecase.subscribe(*get_all_policies())

    create_account_handler(operations[0], a_usecase)
    transaction_handler(operations[1], t_usecase)
    processed = transaction_handler(operations[2], t_usecase)

    expected = {
        "account": {
            "activeCard": True,
            "availableLimit": 60,
            "violations": []
        }
    }
    assert processed == expected


def test_should_verify_card_not_active(repository):
    operations = [
        {"account": {"activeCard": False, "availableLimit": 100}},
        {
            "transaction": {
                "merchant": "Burger King",
                "amount": 20,
                "time": "2019-02-13T10:00:00.000Z"
            }
        },
    ]
    repository.clean()

    a_usecase = AccountUsecase(repository)
    t_usecase = TransactionManager(repository)
    t_usecase.subscribe(*get_all_policies())

    create_account_handler(operations[0], a_usecase)
    processed = transaction_handler(operations[1], t_usecase)

    expected = {
        "account": {
            "activeCard": False,
            "availableLimit": 100,
            "violations": ["card-not-active"]
        }
    }
    assert processed == expected


def test_should_verify_high_frequency_small_interval(repository):
    operations = [
        {"account": {"activeCard": True, "availableLimit": 100}},
        {"transaction": {"merchant": "Burger King 1", "amount": 21, "time": "2019-02-13T10:00:00.000Z"}},
        {"transaction": {"merchant": "Burger King 2", "amount": 22, "time": "2019-02-13T10:00:30.000Z"}},
        {"transaction": {"merchant": "Burger King 3", "amount": 23, "time": "2019-02-13T10:01:00.000Z"}},
        {"transaction": {"merchant": "Burger King 4", "amount": 24, "time": "2019-02-13T10:01:30.000Z"}},
        {"transaction": {"merchant": "Burger King 5", "amount": 25, "time": "2019-02-13T10:02:00.000Z"}},
    ]
    repository.clean()

    a_usecase = AccountUsecase(repository)
    t_usecase = TransactionManager(repository)
    t_usecase.subscribe(*get_all_policies())

    create_account_handler(operations[0], a_usecase)
    transaction_handler(operations[1], t_usecase)
    transaction_handler(operations[2], t_usecase)
    transaction_handler(operations[3], t_usecase)
    processed = transaction_handler(operations[4], t_usecase)

    expected = {
        "account": {
            "activeCard": True,
            "availableLimit": 34,
            "violations": ["high-frequency-small-interval"]
        }
    }
    assert processed == expected


def test_should_verify_subtract_balance_from_account(repository):
    operations = [
        {"account": {"activeCard": True, "availableLimit": 100}},
        {"transaction": {"merchant": "Burger King 1", "amount": 21, "time": "2019-02-13T10:00:00.000Z"}},
        {"transaction": {"merchant": "Burger King 2", "amount": 22, "time": "2019-02-13T10:00:30.000Z"}}
    ]
    repository.clean()

    a_usecase = AccountUsecase(repository)
    t_usecase = TransactionManager(repository)
    t_usecase.subscribe(*get_all_policies())

    create_account_handler(operations[0], a_usecase)
    processed = transaction_handler(operations[1], t_usecase)
    expected = {
        "account": {
            "activeCard": True,
            "availableLimit": 79,
            "violations": []
        }
    }
    assert processed == expected

    processed = transaction_handler(operations[2], t_usecase)
    expected = {
        "account": {
            "activeCard": True,
            "availableLimit": 57,
            "violations": []
        }
    }
    assert processed == expected
