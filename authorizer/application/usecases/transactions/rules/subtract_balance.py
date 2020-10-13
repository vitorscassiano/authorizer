from authorizer.application.usecases.transactions.transaction_interface import TransactionInterface
from authorizer.domain.account import Account
from authorizer.domain.transaction import Transaction
from authorizer.application.exceptions import SubtractBalanceException


class SubtractBalanceTransaction(TransactionInterface):
    def subtract(self, limit, amount):
        return limit - amount

    def execute(
        self,
        account_repository: "Storage",
        transaction_repository: "Storage",
        account: Account,
        transaction: Transaction
    ):
        if not(account):
            raise Exception("account-not-found")

        if(account.availableLimit < transaction.amount):
            raise SubtractBalanceException("insufficient-limit")
        else:
            new_limit = self.subtract(
                account.availableLimit,
                transaction.amount
            )
            new_account = Account(
                activeCard=account.activeCard,
                availableLimit=new_limit
            )
            account_repository.save(new_account)
