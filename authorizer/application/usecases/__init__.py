from authorizer.application.repositories.account_repository import AccountRepository
from authorizer.application.repositories.transaction_repository import TransactionRepository

from authorizer.application.usecases.account import AccountUsecase
from authorizer.application.usecases.transactions.transaction_manager import TransactionManager
from authorizer.application.usecases.transactions.rules import (
    CardNotActiveTransaction,
    HighFrequencySmallInterval,
    DoubledTransaction,
    SubtractBalanceTransaction
)

account_repo = AccountRepository()
transaction_repo = TransactionRepository()

account_usecase = AccountUsecase(account_repo)
transaction_manager = TransactionManager(account_repo, transaction_repo)
transaction_manager.subscribe(
    CardNotActiveTransaction(),
    # HighFrequencySmallInterval(),
    DoubledTransaction(),
    SubtractBalanceTransaction(),
)
