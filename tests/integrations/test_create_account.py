from unittest import TestCase
from authorizer.application.controllers.create_account import CreateAccountController
from authorizer.application.repositories.account_repository import AccountRepository
from authorizer.application.usecases.account import AccountUsecase


class TestCreateAccountController(TestCase):
    def setUp(self):
        repository = AccountRepository()
        usecase = AccountUsecase(repository)
        self.controller = CreateAccountController(usecase)

    def test_should_create_account(self):
        payload = {"account": {"activeCard": True, "availableLimit": 100}}
        response = self.controller.handler(payload)
        self.assertEqual(
            response,
            {
                "activeCard": True,
                "availableLimit": 100,
                "violations": []
            }
        )

    def test_should_not_create_already_initialized_account(self):
        payload = {"account": {"activeCard": True, "availableLimit": 100}}
        first_response = self.controller.handler(payload)
        self.assertEqual(
            first_response,
            {
                "activeCard": True,
                "availableLimit": 100,
                "violations": []
            }
        )
        second_response = self.controller.handler(payload)
        self.assertEqual(
            second_response,
            {
                "activeCard": True,
                "availableLimit": 100,
                "violations": ["account-already-initialized"]
            }
        )
