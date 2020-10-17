# from authorizer.application.repositories.account_repository import AccountRepository
# from authorizer.application.repositories.transaction_repository import TransactionRepository
from authorizer.application.repositories.memory_repository import MemoryRepository

from authorizer.application.usecases.account import AccountUsecase
# from authorizer.application.usecases.transactions.transaction_manager import TransactionManager
# from authorizer.application.usecases.transactions.rules import (
#     CardNotActiveTransaction,
#     HighFrequencySmallInterval,
#     DoubledTransaction,
#     InsufficientLimitTransaction
# )

# account_repo = AccountRepository()
# transaction_repo = TransactionRepository()
# memory_repository = MemoryRepository()
# 
# account_usecase = AccountUsecase(memory_repository)
# transaction_manager = TransactionManager(account_repo, transaction_repo)
# transaction_manager.subscribe(
#     CardNotActiveTransaction(),
#     DoubledTransaction(),
#     InsufficientLimitTransaction(),
#     HighFrequencySmallInterval(),
# )
