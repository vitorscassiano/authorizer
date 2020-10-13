from abc import ABC, abstractmethod
from authorizer.domain.account import Account


class Storage(ABC):
  @abstractmethod
  def is_empty() -> bool: pass
  @abstractmethod
  def save(account: Account) -> None: pass
  @abstractmethod
  def find(account: Account): pass
  @abstractmethod
  def remove(account: Account) -> None: pass
