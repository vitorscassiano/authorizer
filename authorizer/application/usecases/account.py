from authorizer.domain.account import Account
from authorizer.application.repositories.memory_repository import MemoryRepository


class AccountUsecase:
    def __init__(self, repository: MemoryRepository):
        self.repository = repository

    def create(self, active_card, available_limit):
        if(self.repository.is_account_empty()):
            account = Account(active_card, available_limit)
            self.repository.save_account(account)
            return account
        else:
            found = self.repository.find_account()
            return Account(
                activeCard=found.activeCard,
                availableLimit=found.availableLimit,
                violations=["account-already-initialized"]
            )
