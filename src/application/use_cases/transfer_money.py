"""
Use Case: Transferir dinheiro entre contas.

IMPORTANTE: Este Use Case NÃO executa a transferência imediatamente!
Ele publica um evento TransferRequested na fila (RabbitMQ).
Um WORKER vai processar a transferência de forma assíncrona.

Fluxo:
1. Valida que ambas as contas existem
2. Publica evento TransferRequested na fila
3. Retorna "transferência em processamento"
4. Worker processa depois (fora deste Use Case)
"""

from dataclasses import dataclass
import uuid

from ...domain.value_objects import AccountNumber, Money
from ...domain.events import TransferRequested
from ..interfaces import AccountRepository, EventPublisher


@dataclass
class TransferMoneyInput:
    """Dados de entrada para transferência."""
    from_account_number: str
    to_account_number: str
    amount: float


@dataclass
class TransferMoneyOutput:
    """Dados de saída após solicitar transferência."""
    transfer_id: str
    from_account: str
    to_account: str
    amount: str
    status: str  # "processing"


class TransferMoneyUseCase:
    """
    Caso de uso: Solicitar transferência.
    
    NÃO executa a transferência! Apenas publica na fila.
    """
    
    def __init__(
        self,
        account_repository: AccountRepository,
        event_publisher: EventPublisher,
    ) -> None:
        self.account_repository = account_repository
        self.event_publisher = event_publisher
    
    async def execute(self, input_dto: TransferMoneyInput) -> TransferMoneyOutput:
        """
        Solicita uma transferência (envia para fila).
        
        Args:
            input_dto: Dados da transferência
            
        Returns:
            ID da transferência e status "processing"
            
        Raises:
            ValueError: Se contas não existirem ou dados inválidos
        """
        # 1. Converter para Value Objects
        from_account_number = AccountNumber(value=input_dto.from_account_number)
        to_account_number = AccountNumber(value=input_dto.to_account_number)
        amount = Money.create(input_dto.amount)
        
        # 2. Validar que não é a mesma conta
        if from_account_number == to_account_number:
            raise ValueError("Não é possível transferir para a mesma conta")
        
        # 3. Validar que ambas as contas existem
        from_account = await self.account_repository.find_by_account_number(
            from_account_number
        )
        if not from_account:
            raise ValueError(f"Conta origem {from_account_number} não encontrada")
        
        to_account = await self.account_repository.find_by_account_number(
            to_account_number
        )
        if not to_account:
            raise ValueError(f"Conta destino {to_account_number} não encontrada")
        
        # 4. Gerar ID único para a transferência
        transfer_id = str(uuid.uuid4())
        
        # 5. Publicar evento na FILA (RabbitMQ)
        # O Worker vai processar este evento depois!
        event = TransferRequested(
            transfer_id=transfer_id,
            from_account=str(from_account_number),
            to_account=str(to_account_number),
            amount=str(amount.amount),
        )
        await self.event_publisher.publish(event)
        
        # 6. Retornar "em processamento" (não foi executada ainda!)
        return TransferMoneyOutput(
            transfer_id=transfer_id,
            from_account=str(from_account_number),
            to_account=str(to_account_number),
            amount=str(amount.amount),
            status="processing",  # ← Importante! Ainda não foi processada
        )