from abc import ABC, abstractmethod
from authorizer.application.repositories.storage import Storage


class TransactionInterface(ABC):
    @abstractmethod
    def execute(
        self,
        account_repository: Storage,
        transaction_repository: Storage,
        account_dto: dict,
        transaction_dto: dict
    ):
        pass
