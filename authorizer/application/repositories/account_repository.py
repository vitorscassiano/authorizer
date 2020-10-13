from authorizer.domain.account import Account


class AccountRepository:
  def __init__(self):
    self.db = []

  def is_empty(self):
    return bool(len(self.db) <= 0)

  def save(self, account: Account) -> None:
    self.db.append(account)

  def find(self) -> Account:
    return self.db[0]

  def remove(self, account: Account) -> None:
    self.db.remove(account)
