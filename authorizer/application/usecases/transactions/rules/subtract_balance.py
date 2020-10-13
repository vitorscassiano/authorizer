from authorizer.application.usecases.transactions.transaction_interface import TransactionInterface
from authorizer.domain.account import Account
from authorizer.domain.transaction import Transaction


class SubtractBalanceTransaction(TransactionInterface):
  def execute(
      self,
      account_repository: "Storage",
      transaction_repository: "Storage",
      transaction_dto: dict
  ):
    account = account_repository.find()
    transaction = Transaction(**transaction_dto)
    if not(account):
      raise Exception("account-not-found")

    if(account.availableLimit < transaction.amount):
      account.violations = [
          *account.violations,
          "insufficient-limit"
      ]
      account_repository.save(account)
      raise Exception("insufficient-limit")
    else:
      account.availableLimit = account.availableLimit - transaction.amount
      account_repository.save(account)
