from abc import ABC, abstractmethod
from typing import Optional

from ...domain.entities import Account
from ...domain.value_objects import AccountNumber, CPF

class AccountRepository(ABC):

    @abstractmethod
    async def save(self, account: Account) -> None:
        pass

    @abstractmethod
    async def find_by_account_number(self, account_number: AccountNumber) -> Optional[Account]:
        pass

    @abstractmethod
    async def find_by_cpf(self, cpf: CPF) -> Optional[Account]:
        pass

    @abstractmethod
    async def exists_by_cpf(self, cpf: CPF) -> bool:
        pass

    @abstractmethod
    async def delete(self, account_number: AccountNumber) -> None:
        pass