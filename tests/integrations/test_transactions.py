from unittest import TestCase, skip
from authorizer.application.controllers.transaction import PipelineTransactionController
from authorizer.application.usecases.transactions.transaction_manager import TransactionManager
from authorizer.application.repositories.account_repository import AccountRepository
from authorizer.application.repositories.transaction_repository import TransactionRepository
from authorizer.application.usecases.transactions.rules import (
    CardNotActiveTransaction,
    HighFrequencySmallInterval,
    DoubledTransaction,
    SubtractBalanceTransaction
)

from authorizer.application.repositories.account_repository import AccountRepository
from authorizer.application.usecases.account import AccountUsecase

class TestPipelineTransactions(TestCase):
    def setUp(self):
        account_repository = AccountRepository()
        account_usecase = AccountUsecase(account_repository)
        transaction_repository = TransactionRepository()
        manager = TransactionManager(
            account_repository,
            transaction_repository
        )
        transaction_controller = PipelineTransactionController(transaction_manager, account_usecase)
        transaction_manager.subscribe(
            CardNotActiveTransaction(),
            # HighFrequencySmallInterval(),
            DoubledTransaction(),
            SubtractBalanceTransaction(),
        )

    @skip("not implemented")
    def test_should_validate_card_not_activated(self): pass
    @skip("not implemented")
    def test_should_validate_doubled_transaction(self): pass
    @skip("not implemented")
    def test_should_validate_high_frequency_small_interval(self): pass
    @skip("not implemented")
    def test_should_validate_insufficient_limit(self): pass
    @skip("not implemented")
    def test_should_validate_subtract_successfully(self): pass
