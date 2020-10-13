class CreateAccountController:
  def __init__(self, account_usecase: "AccountUsecases"):
    self.account_usecase = account_usecase

  def handler(self, data):
      account = data["account"]
      account = self.account_usecase.create(
        active_card=account["activeCard"],
        available_limit=account["availableLimit"]
      )
      return account.to_json()
      # print(account)
