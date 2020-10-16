from authorizer.application.usecases.transactions.transaction_interface import TransactionInterface
from authorizer.domain.account import Account
from authorizer.domain.transaction import Transaction
from authorizer.application.exceptions import InsufficientLimitException


class InsufficientLimitTransaction(TransactionInterface):
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
            raise InsufficientLimitException("insufficient-limit")
