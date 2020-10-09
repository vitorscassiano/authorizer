from abc import ABC, abstractmethod
from authorizer.domain.account import Account


class Storage(ABC):
  @abstractmethod
  def save(account: Account): pass
  @abstractmethod
  def find(account: Account): pass
  @abstractmethod
  def remove(account: Account): pass
