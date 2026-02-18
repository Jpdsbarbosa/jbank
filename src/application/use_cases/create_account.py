"""
Use Case: Criar uma nova conta bancária.

Este Use Case coordena a criação de uma conta:
1. Valida se CPF já não existe
2. Cria a entidade Account (domínio faz as validações!)
3. Salva no repositório
4. Dispara evento AccountCreated
"""

from dataclasses import dataclass

from ...domain.entities import Account
from ...domain.value_objects import CPF, Money
from ...domain.events import AccountCreated
from ..interfaces import AccountRepository, EventPublisher



@dataclass
class CreateAccountInput:
    """
    DTO (Data Transfer Object) com os dados de entrada.
    
    Isola a camada de Application da API/Presentation.
    """
    holder_name: str
    cpf: str
    initial_balance: float


@dataclass
class CreateAccountOutput:
    """
    DTO com os dados de saída.
    
    O que retornamos para quem chamou o Use Case.
    """
    account_number: str
    holder_name: str
    cpf: str
    balance: str
    status: str


class CreateAccountUseCase:
    """
    Caso de uso: Criar conta bancária.
    
    Recebe as dependências via construtor (Dependency Injection).
    """
    
    def __init__(
        self,
        account_repository: AccountRepository,
        event_publisher: EventPublisher,
    ) -> None:
        """
        Injeta as dependências.
        
        Args:
            account_repository: Repositório de contas (interface!)
            event_publisher: Publicador de eventos (interface!)
        """
        self.account_repository = account_repository
        self.event_publisher = event_publisher
    
    async def execute(self, input_dto: CreateAccountInput) -> CreateAccountOutput:
        """
        Executa o caso de uso.
        
        Args:
            input_dto: Dados de entrada
            
        Returns:
            Dados da conta criada
            
        Raises:
            ValueError: Se CPF já existir ou dados inválidos
        """
        # 1. Converter strings para Value Objects (com validação!)
        cpf = CPF(input_dto.cpf)
        initial_balance = Money.create(input_dto.initial_balance)
        
        # 2. Verificar se CPF já existe
        exists = await self.account_repository.exists_by_cpf(cpf)
        if exists:
            raise ValueError(f"CPF {cpf} já possui uma conta cadastrada")
        
        # 3. Criar a entidade (lógica de negócio no domínio!)
        account = Account.create(
            holder_name=input_dto.holder_name,
            cpf=cpf,
            initial_balance=initial_balance,
        )
        
        # 4. Salvar no repositório
        await self.account_repository.save(account)
        
        # 5. Disparar evento de domínio
        event = AccountCreated(
            account_number=str(account.account_number),
            holder_name=account.holder_name,
            cpf=str(account.cpf),
            initial_balance=str(account.balance.amount),
        )
        await self.event_publisher.publish(event)
        
        # 6. Retornar dados da conta criada
        return CreateAccountOutput(
            account_number=str(account.account_number),
            holder_name=account.holder_name,
            cpf=str(account.cpf),
            balance=str(account.balance.amount),
            status=account.status.value,
        )
