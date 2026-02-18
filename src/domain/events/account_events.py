from dataclasses import dataclass, field
from datetime import datetime

from .base import DomainEvent

@dataclass(frozen=True)
class AccountCreated(DomainEvent):
    account_number: str = field(kw_only=True)
    holder_name: str = field(kw_only=True)
    cpf: str = field(kw_only=True)
    initial_balance: str = field(kw_only=True)

    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        base_dict.update({
            "account_number": self.account_number,
            "holder_name": self.holder_name,
            "cpf": self.cpf,
            "initial_balance": self.initial_balance,
        })
        return base_dict

@dataclass(frozen=True)
class AccountApproved(DomainEvent):
    account_number: str = field(kw_only=True)

    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        base_dict["account_number"] = self.account_number
        return base_dict

@dataclass(frozen=True)
class AccountRejected(DomainEvent):
    account_number: str = field(kw_only=True)
    reason: str = field(default="", kw_only=True)

    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        base_dict.update({
            "account_number": self.account_number,
            "reason": self.reason,
        })
        return base_dict

@dataclass(frozen=True)
class AccountBlocked(DomainEvent):
    account_number: str = field(kw_only=True)
    reason: str = field(default="", kw_only=True)

    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        base_dict.update({
            "account_number": self.account_number,
            "reason": self.reason,
        })
        return base_dict

@dataclass(frozen=True)
class AccountClosed(DomainEvent):
    account_number: str = field(kw_only=True)

    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        base_dict["account_number"] = self.account_number
        return base_dict

@dataclass(frozen=True)
class MoneyDeposited(DomainEvent):
    account_number: str = field(kw_only=True)
    amount: str = field(kw_only=True)
    new_balance: str = field(kw_only=True)

    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        base_dict.update({
            "account_number": self.account_number,
            "amount": self.amount,
            "new_balance": self.new_balance,
        })
        return base_dict

@dataclass(frozen=True)
class MoneyWithdrawn(DomainEvent):
    account_number: str = field(kw_only=True)
    amount: str = field(kw_only=True)
    new_balance: str = field(kw_only=True)

    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        base_dict.update({
            "account_number": self.account_number,
            "amount": self.amount,
            "new_balance": self.new_balance,
        })
        return base_dict