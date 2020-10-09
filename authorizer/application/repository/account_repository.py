from authorizer.application.repository.storage import Storage
from authorizer.domain.account import Account


class AccountRepository(Storage):
  def __init__(self):
    self.db = []

  def save(self, account: Account) -> None:
    self.db.append(account)

  def find(self, account: Account) -> Account:
    return self.db.find(account)

  def remove(self) -> None:
    self.db.remove(account)
