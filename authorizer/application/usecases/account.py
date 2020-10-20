from authorizer.domain.account import Account
from authorizer.application.repositories.memory_repository \
    import MemoryRepository


class AccountUsecase:
    def __init__(self, repository: MemoryRepository):
        self.repository = repository

    def create(self, active_card: bool, available_limit: int) -> Account:
        found = self.repository.find_account()
        if not(found):
            account = Account(active_card, available_limit)
            self.repository.save_account(account)
            return account
        else:
            return Account(
                activeCard=found.activeCard,
                availableLimit=found.availableLimit,
                violations=["account-already-initialized"]
            )
