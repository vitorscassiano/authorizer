from authorizer.domain.account import Account
from authorizer.domain.transaction import Transaction
from authorizer.application.repositories import MemoryRepository
from authorizer.application.usecases.transactions.transaction_interface \
    import TransactionInterface


class CardNotActivePolicy(TransactionInterface):
    @staticmethod
    def execute(
        repository: MemoryRepository,
        account: Account,
        transaction: Transaction
    ):
        if not(account.activeCard):
            return ["card-not-active"]
        return []
