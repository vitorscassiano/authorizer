from authorizer.domain.account import Account
from authorizer.domain.transaction import Transaction
from authorizer.application.exceptions import InsufficientLimitException
from authorizer.application.usecases.transactions.transaction_interface import TransactionInterface


class InsufficientLimitPolicy(TransactionInterface):
    @staticmethod
    def execute(repository, account: Account, transaction: Transaction):
        if(account.availableLimit < transaction.amount):
            raise InsufficientLimitException("insufficient-limit")
