from abc import ABCMeta, abstractmethod
from authorizer.domain.account import Account
from authorizer.domain.transaction import Transaction
from authorizer.application.repositories import MemoryRepository


class abstractstatic(staticmethod):
    __slots__ = ()

    def __init__(self, function):
        super(abstractstatic, self).__init__(function)
        function.__isabstractmethod__ = True
    __isabstractmethod__ = True


class TransactionInterface(object):
    __metaclass__ = ABCMeta

    @abstractstatic
    def execute(
        self,
        repository: MemoryRepository,
        account: Account,
        transaction: Transaction
    ): pass
