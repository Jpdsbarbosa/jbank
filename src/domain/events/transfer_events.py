from dataclasses import dataclass, field

from .base import DomainEvent

@dataclass(frozen=True)
class TransferRequested(DomainEvent):
    transfer_id: str = field(kw_only=True)
    from_account: str = field(kw_only=True)
    to_account: str = field(kw_only=True)
    amount: str = field(kw_only=True)

    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        base_dict.update({
            "transfer_id": self.transfer_id,
            "from_account": self.from_account,
            "to_account": self.to_account,
            "amount": self.amount,
        })
        return base_dict

@dataclass(frozen=True)
class TransferCompleted(DomainEvent):
    transfer_id: str = field(kw_only=True)
    from_account: str = field(kw_only=True)
    to_account: str = field(kw_only=True)
    amount: str = field(kw_only=True)

    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        base_dict.update({
            "transfer_id": self.transfer_id,
            "from_account": self.from_account,
            "to_account": self.to_account,
            "amount": self.amount,
        })
        return base_dict
        
@dataclass(frozen=True)
class TransferFailed(DomainEvent):
    transfer_id: str = field(kw_only=True)
    from_account: str = field(kw_only=True)
    to_account: str = field(kw_only=True)
    amount: str = field(kw_only=True)
    reason: str = field(default="", kw_only=True)

    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        base_dict.update({
            "transfer_id": self.transfer_id,
            "from_account": self.from_account,
            "to_account": self.to_account,
            "amount": self.amount,
            "reason": self.reason,
        })
        return base_dict