from abc import ABC, abstractmethod
from typing import List, Any
from authorizer.domain.account import Account


class Storage(ABC):
  @abstractmethod
  def is_empty() -> bool: pass
  @abstractmethod
  def save(data: Any) -> None: pass
  @abstractmethod
  def find(data: Any) -> Any: pass
  @abstractmethod
  def remove(data: Any) -> None: pass
  @abstractmethod
  def find_all() -> List[Any]: pass
