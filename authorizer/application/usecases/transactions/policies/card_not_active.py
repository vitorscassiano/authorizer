from authorizer.application.usecases.transactions.transaction_interface import TransactionInterface
from authorizer.application.exceptions import CardNotActiveException
from authorizer.domain.account import Account
from authorizer.domain.transaction import Transaction


class CardNotActivePolicy(TransactionInterface):
    @staticmethod
    def execute(repository, account: Account, transaction: Transaction):
        if(account):
            if not(account.activeCard):
                raise CardNotActiveException("card-not-active")
        else:
            raise Exception("account-not-found")
