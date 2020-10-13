class PipelineTransactionController():
  def __init__(self, transaction_manager: "TransactionManager", account_usecase):
    self.transaction_manager = transaction_manager
    self.account_usecase = account_usecase

  def handler(self, data):
      transaction = data["transaction"]
      self.transaction_manager.notify(transaction)
      account = self.account_usecase.find()
      print(account)