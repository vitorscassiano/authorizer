from dataclasses import dataclass


@dataclass
class Transaction:
  merchant: str = ""
  amount: int = 0
  time: str = ""
