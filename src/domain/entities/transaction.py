from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import uuid

from ..value_objects import AccountNumber, Money

class TransactionType(Enum):
    DEPOSIT = "deposit"
    WITHDRAW = "withdraw"
    TRANSFER_OUT = "transfer_out"
    TRANSFER_IN = "transfer_in"
    
class TransactionStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    
@dataclass
class Transaction:
    id: str
    account_number: AccountNumber
    type: TransactionType
    amount: Money
    status: TransactionStatus
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: datetime | None = None
    description: str = ""
    related_account: AccountNumber | None = None

    @staticmethod
    def create(
        account_number: AccountNumber,
        type: TransactionType,
        amount: Money,
        description: str = "",
        related_account: AccountNumber | None = None,
    ) -> "Transaction":
        return Transaction(
            id=str(uuid.uuid4()),
            account_number=account_number,
            type=type,
            amount=amount,
            status=TransactionStatus.PENDING,
            description=description,
            related_account=related_account,
        )
    
    def complete(self) -> None:
        if self.status != TransactionStatus.PENDING:
            raise ValueError(f"Cannot complete: {self.id} is not pending")
        self.status = TransactionStatus.COMPLETED
        self.completed_at = datetime.now()

    def fail(self, reason: str) -> None:
        if self.status != TransactionStatus.PENDING:
            raise ValueError(f"Cannot fail: transaction is {self.status.value}")
        self.status = TransactionStatus.FAILED
        self.completed_at = datetime.now()
        if reason:
            self.description = reason

    def cancel(self) -> None:
        if self.status != TransactionStatus.PENDING:
            raise ValueError(f"Cannot cancel: transaction is {self.status.value}")
        self.status = TransactionStatus.CANCELLED
        self.completed_at = datetime.now()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Transaction):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def __repr__(self) -> str:
        return(
            f"Transaction(id={self.id}, "
            f"account_number={self.account_number}, "
            f"type={self.type}, "
            f"amount={self.amount}, "
            f"status={self.status}, "
            f"completed_at={self.completed_at}, "
            )