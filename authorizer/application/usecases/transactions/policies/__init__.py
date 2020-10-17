from authorizer.application.usecases.transactions.policies.card_not_active import CardNotActivePolicy
from authorizer.application.usecases.transactions.policies.high_frequency_small_interval import HighFrequencyPolicy
from authorizer.application.usecases.transactions.policies.doubled import DoubledPolicy
from authorizer.application.usecases.transactions.policies.insufficient_limit import InsufficientLimitPolicy


def get_all_policies():
  return [
    CardNotActivePolicy,
    HighFrequencyPolicy,
    DoubledPolicy,
    InsufficientLimitPolicy
  ]