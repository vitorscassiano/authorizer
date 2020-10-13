from dataclasses import dataclass, field, asdict


@dataclass
class Account:
    activeCard: bool = True
    availableLimit: int = 0
    violations: list = field(default_factory=list)

    def to_json(self):
        return asdict(self)
