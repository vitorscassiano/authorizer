from authorizer.application.usecases.transactions.transaction_interface import TransactionInterface


class CardNotActiveException(Exception):
  pass


class CardNotActiveTransaction(TransactionInterface):
  def execute(
      self,
      account_repository: "Storage",
      transaction_repository: "Storage",
      transaction_dto: dict
  ):
    account = account_repository.find()
    if not(account):
      raise Exception("account-not-found")

    if not(account.active_card):
      account.violations = [
          *account.violations,
          "card-not-active"
      ]
      account_repository.save(account)
      raise Exception("card-not-active")
