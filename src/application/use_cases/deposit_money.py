"""
Use Case: Depositar dinheiro em uma conta.

Fluxo:
1. Busca a conta
2. Deposita o dinheiro (lógica na entidade!)
3. Salva no repositório
4. Dispara evento MoneyDeposited
"""

from dataclasses import dataclass

from ...domain.value_objects import AccountNumber, Money
from ...domain.events import MoneyDeposited
from ..interfaces import AccountRepository, EventPublisher


@dataclass
class DepositMoneyInput:
    """Dados de entrada para depósito."""
    account_number: str
    amount: float


@dataclass
class DepositMoneyOutput:
    """Dados de saída após depósito."""
    account_number: str
    old_balance: str
    amount_deposited: str
    new_balance: str


class DepositMoneyUseCase:
    """Caso de uso: Depositar dinheiro."""
    
    def __init__(
        self,
        account_repository: AccountRepository,
        event_publisher: EventPublisher,
    ) -> None:
        self.account_repository = account_repository
        self.event_publisher = event_publisher
    
    async def execute(self, input_dto: DepositMoneyInput) -> DepositMoneyOutput:
        """
        Executa o depósito.
        
        Args:
            input_dto: Dados do depósito
            
        Returns:
            Resultado do depósito
            
        Raises:
            ValueError: Se conta não existir ou dados inválidos
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
        
        # 4. Depositar (lógica na entidade!)
        account.deposit(amount)
        
        # 5. Salvar no repositório
        await self.account_repository.save(account)
        
        # 6. Disparar evento
        event = MoneyDeposited(
            account_number=str(account.account_number),
            amount=str(amount.amount),
            new_balance=str(account.balance.amount),
        )
        await self.event_publisher.publish(event)
        
        # 7. Retornar resultado
        return DepositMoneyOutput(
            account_number=str(account.account_number),
            old_balance=str(old_balance.amount),
            amount_deposited=str(amount.amount),
            new_balance=str(account.balance.amount),
        )