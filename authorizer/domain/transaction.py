from dataclasses import dataclass


@dataclass
class Transaction:
    merchant: str = ""
    amount: int = 0
    time: str = ""

    def __eq__(self, other):
        if isinstance(other, Transaction):
            return bool(
                (self.merchant == other.merchant) and
                (self.amount == other.amount)
            )
        return False
