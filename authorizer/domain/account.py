from dataclasses import dataclass


@dataclass
class Account:
  card_active: bool
  available_limit: int
  violations: list
  history: list
