from authorizer.application.repositories.storage import Storage
from authorizer.application.repositories.account_repository import AccountRepository
from authorizer.domain.account import Account
from authorizer.domain.transaction import Transaction


class AccountUsecase:
    def __init__(self, repository):
        self.repository = repository

    def create(self, active_card, available_limit):
        account = Account(
            activeCard=active_card,
            availableLimit=available_limit
        )
        if (self.repository.is_empty()):
            self.repository.save(account)
            return account
        else:
            found = self.repository.find()
            found.violations = ["account-already-initialized"]
            self.repository.save(found)
            return found

    def find(self):
        account = self.repository.find()
        return account

