"""Use Cases (Casos de Uso) da aplicação."""

from .create_account import (
    CreateAccountUseCase,
    CreateAccountInput,
    CreateAccountOutput,
)
from .deposit_money import (
    DepositMoneyUseCase,
    DepositMoneyInput,
    DepositMoneyOutput,
)
from .withdraw_money import (
    WithdrawMoneyUseCase,
    WithdrawMoneyInput,
    WithdrawMoneyOutput,
)
from .transfer_money import (
    TransferMoneyUseCase,
    TransferMoneyInput,
    TransferMoneyOutput,
)

__all__ = [
    "CreateAccountUseCase",
    "CreateAccountInput",
    "CreateAccountOutput",
    "DepositMoneyUseCase",
    "DepositMoneyInput",
    "DepositMoneyOutput",
    "WithdrawMoneyUseCase",
    "WithdrawMoneyInput",
    "WithdrawMoneyOutput",
    "TransferMoneyUseCase",
    "TransferMoneyInput",
    "TransferMoneyOutput",
]