"""Eventos de domínio do sistema bancário."""

from .base import DomainEvent
from .account_events import (
    AccountCreated,
    AccountApproved,
    AccountRejected,
    AccountBlocked,
    AccountClosed,
    MoneyDeposited,
    MoneyWithdrawn,
)
from .transfer_events import (
    TransferRequested,
    TransferCompleted,
    TransferFailed,
)

__all__ = [
    "DomainEvent",
    "AccountCreated",
    "AccountApproved",
    "AccountRejected",
    "AccountBlocked",
    "AccountClosed",
    "MoneyDeposited",
    "MoneyWithdrawn",
    "TransferRequested",
    "TransferCompleted",
    "TransferFailed",
]