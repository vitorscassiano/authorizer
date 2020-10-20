from authorizer.application.usecases.account import AccountUsecase
from authorizer.application.repositories.memory_repository \
    import MemoryRepository
from authorizer.application.usecases.transactions.transaction_manager \
    import TransactionManager
from authorizer.application.usecases.transactions.policies \
    import get_all_policies

memory_repository = MemoryRepository()
account_usecase = AccountUsecase(memory_repository)
transaction_manager = TransactionManager(memory_repository)
transaction_manager.subscribe(*get_all_policies())
