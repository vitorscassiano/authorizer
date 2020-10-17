from authorizer.application.controllers.create_account import create_account_handler
from authorizer.application.repositories import MemoryRepository
from authorizer.application.usecases import AccountUsecase


def test_sould_create_account():
    operations = {"account": {"activeCard": True, "availableLimit": 100}}

    usecase = AccountUsecase(MemoryRepository())
    processed = create_account_handler(operations, usecase)

    expected = {
        "account": {
            "activeCard": True,
            "availableLimit": 100,
            "violations": []
        }
    }
    assert processed == expected


def test_should_not_create_already_initialized_account():
    operations = {"account": {"activeCard": True, "availableLimit": 100}}

    usecase = AccountUsecase(MemoryRepository())
    create_account_handler(operations, usecase)
    processed = create_account_handler(operations, usecase)

    expected = {
        "account": {
            "activeCard": True,
            "availableLimit": 100,
            "violations": ["account-already-initialized"]
        }
    }
    assert processed == expected
