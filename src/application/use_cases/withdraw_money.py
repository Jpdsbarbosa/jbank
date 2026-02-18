"""
Use Case: Sacar dinheiro de uma conta.

Fluxo:
1. Busca a conta
2. Saca o dinheiro (lógica na entidade valida saldo!)
3. Salva no repositório
4. Dispara evento MoneyWithdrawn
"""

from dataclasses import dataclass

from ...domain.value_objects import AccountNumber, Money
from ...domain.events import MoneyWithdrawn
from ..interfaces import AccountRepository, EventPublisher


@dataclass
class WithdrawMoneyInput:
    """Dados de entrada para saque."""
    account_number: str
    amount: float


@dataclass
class WithdrawMoneyOutput:
    """Dados de saída após saque."""
    account_number: str
    old_balance: str
    amount_withdrawn: str
    new_balance: str


class WithdrawMoneyUseCase:
    """Caso de uso: Sacar dinheiro."""
    
    def __init__(
        self,
        account_repository: AccountRepository,
        event_publisher: EventPublisher,
    ) -> None:
        self.account_repository = account_repository
        self.event_publisher = event_publisher
    
    async def execute(self, input_dto: WithdrawMoneyInput) -> WithdrawMoneyOutput:
        """
        Executa o saque.
        
        Args:
            input_dto: Dados do saque
            
        Returns:
            Resultado do saque
            
        Raises:
            ValueError: Se conta não existir, saldo insuficiente ou dados inválidos
        """
        # 1. Converter para Value Objects
        account_number = AccountNumber(value=input_dto.account_number)
        amount = Money.create(input_dto.amount)
        
        # 2. Buscar a conta
        account = await self.account_repository.find_by_account_number(
            account_number
        )
        if not account:
            raise ValueError(f"Conta {account_number} não encontrada")
        
        # 3. Guardar saldo antigo
        old_balance = account.balance
        
        # 4. Sacar (entidade valida saldo e status!)
        account.withdraw(amount)
        
        # 5. Salvar no repositório
        await self.account_repository.save(account)
        
        # 6. Disparar evento
        event = MoneyWithdrawn(
            account_number=str(account.account_number),
            amount=str(amount.amount),
            new_balance=str(account.balance.amount),
        )
        await self.event_publisher.publish(event)
        
        # 7. Retornar resultado
        return WithdrawMoneyOutput(
            account_number=str(account.account_number),
            old_balance=str(old_balance.amount),
            amount_withdrawn=str(amount.amount),
            new_balance=str(account.balance.amount),
        )