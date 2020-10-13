from authorizer.application.usecases.transactions.transaction_interface import TransactionInterface
from authorizer.domain.account import Account
from authorizer.domain.transaction import Transaction

from datetime import datetime


class HighFrequencySmallInterval(TransactionInterface):
  TIME_TOKEN = "%Y-%m-%dT%H:%M:%S.%f%z"

  def minutes(self, delta: datetime):
    return delta.seconds/60

  def is_doubled(self, last_transaction: Transaction, current_transaction: Transaction):
    last_transaction_time = datetime.strptime(
        last_transaction.time, self.TIME_TOKEN)
    current_transaction_time = datetime.strptime(
        current_transaction.time, self.TIME_TOKEN)
    delta = current_transaction_time - last_transaction_time

    if(delta.days <= 0):
      return bool(self.minutes(delta) <= 2)
    else:
      False

  def execute(
      self,
      account_repository,
      transaction_repository,
      transaction_dto
  ):
    transaction = Transaction(**transaction_dto)
    account = account_repository.find()
    transactions = transaction_repository.find()
    if(len(transactions) > 0):
      last_transaction = transactions[-1]

    if((transaction.merchant == last_transaction.merchant) and (transaction.amount == last_transaction.amount)):
      if(self.is_doubled(last_transaction, transaction)):
        account.violations = [
            *account.violations,
            "doubled-transaction"
        ]
        account_repository.save(account)
