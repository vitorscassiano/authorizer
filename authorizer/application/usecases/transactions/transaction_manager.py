from authorizer.application.repositories.storage import Storage
from authorizer.application.usecases.account import AccountUsecase
from authorizer.domain.transaction import Transaction


class TransactionManager():
  def __init__(self, account_repo, transaction_repo):
    self.subscriptions = []
    self.account_repo = account_repo
    self.transaction_repo = transaction_repo

  def subscribe(self, *transactions):
    for transaction in transactions:
      self.subscriptions.append(transaction)

  def unsubscribe(self, *transactions):
    for transaction in transactions:
      self.subscriptions.remove(transaction)

  def notify(self, transaction_dto: dict):
    try:
      for subscription in self.subscriptions:
        subscription.execute(
            self.account_repo, self.transaction_repo, transaction_dto)
      transaction = Transaction(**transaction_dto)
      self.transaction_repo.save(transaction)
    except Exception as e:
      pass
