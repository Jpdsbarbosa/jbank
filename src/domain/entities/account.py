from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from enum import Enum

from ..value_objects import AccountNumber, CPF, Money

class AccountStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    BLOCKED = "blocked"
    ANALYSIS = "analysis"
    CLOSED = "closed"

@dataclass
class Account:
    account_number: AccountNumber
    holder_name: str
    cpf: CPF
    balance: Money
    status: AccountStatus
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    @staticmethod
    def create(holder_name: str, cpf: CPF, initial_balance: Money) -> "Account":
        return Account(
            account_number=AccountNumber.generate(),
            holder_name=holder_name,
            cpf=cpf,
            balance=initial_balance,
            status=AccountStatus.ANALYSIS,
        )

    def deposit(self, amount: Money) -> None:
        if self.status != AccountStatus.ACTIVE:
            raise ValueError(f"Account {self.account_number} is not active")

        self.balance = self.balance.add(amount)
        self.updated_at = datetime.now()

    def withdraw(self, amount: Money) -> None:
        if self.status != AccountStatus.ACTIVE:
            raise ValueError(f"Account {self.account_number} is not active")
        self.balance = self.balance.subtract(amount)
        self.updated_at = datetime.now()

    def block(self) -> None:
        if self.status == AccountStatus.BLOCKED:
            raise ValueError(f"Account {self.account_number} is already blocked")
        self.status = AccountStatus.BLOCKED
        self.updated_at = datetime.now()

    def unblock(self) -> None:
        if self.status == AccountStatus.ACTIVE:
            raise ValueError(f"Account {self.account_number} is already active")
        self.status = AccountStatus.ACTIVE
        self.updated_at = datetime.now()
    
    def close(self) -> None:
        if self.status == AccountStatus.CLOSED:
            raise ValueError(f"Account {self.account_number} is already closed")
        self.status = AccountStatus.CLOSED
        self.updated_at = datetime.now()
    
    def approve(self) -> None:
        if self.status not in [AccountStatus.ANALYSIS, AccountStatus.BLOCKED]:
            raise ValueError(f"Account {self.account_number} is not in analysis or blocked")
        self.status = AccountStatus.ACTIVE
        self.updated_at = datetime.now()

    def reject(self) -> None:
        if self.status != AccountStatus.ANALYSIS:
            raise ValueError(f"Account {self.account_number} is not in analysis")
        self.status = AccountStatus.INACTIVE
        self.updated_at = datetime.now()

    def reactivate(self) -> None:
        if self.status not in [AccountStatus.INACTIVE, AccountStatus.BLOCKED]:
            raise ValueError(f"Account {self.account_number} is not inactive or blocked")
        self.status = AccountStatus.ACTIVE
        self.updated_at = datetime.now()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Account):
            return False
        return self.account_number == other.account_number

    def __hash__(self) -> int:
        return hash(self.account_number)

    def __repr__(self) -> str:
        return(
            f"Account(number={self.account_number}, "
            f"holder_name={self.holder_name}, "
            f"cpf={self.cpf}, "
            f"balance={self.balance}, "
            f"status={self.status}, "
            f"created_at={self.created_at}, "
            f"updated_at={self.updated_at})"
        )
    