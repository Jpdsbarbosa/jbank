"""
Dependency Injection para FastAPI.

Fornece instâncias de repositórios e publishers para as rotas.
"""

from typing import Annotated
from fastapi import Depends

from src.infrastructure.config import settings
from src.infrastructure.database import MongoAccountRepository
from src.infrastructure.messaging import RabbitMQEventPublisher
from src.application.use_cases import (
    CreateAccountUseCase,
    DepositMoneyUseCase,
    WithdrawMoneyUseCase,
    TransferMoneyUseCase,
)


# ==================== REPOSITÓRIOS ====================

def get_account_repository() -> MongoAccountRepository:
    """Fornece instância do repositório de contas."""
    return MongoAccountRepository(
        mongodb_url=settings.mongodb_url,
        database_name=settings.mongodb_database,
    )


# ==================== EVENT PUBLISHER ====================

async def get_event_publisher() -> RabbitMQEventPublisher:
    """Fornece instância do event publisher."""
    publisher = RabbitMQEventPublisher(
        rabbitmq_url=settings.rabbitmq_url,
        exchange_name=settings.rabbitmq_exchange,
    )
    await publisher.connect()
    return publisher


# ==================== USE CASES ====================

async def get_create_account_use_case(
    repository: Annotated[MongoAccountRepository, Depends(get_account_repository)],
    publisher: Annotated[RabbitMQEventPublisher, Depends(get_event_publisher)],
) -> CreateAccountUseCase:
    """Fornece instância do use case de criar conta."""
    return CreateAccountUseCase(repository, publisher)


async def get_deposit_money_use_case(
    repository: Annotated[MongoAccountRepository, Depends(get_account_repository)],
    publisher: Annotated[RabbitMQEventPublisher, Depends(get_event_publisher)],
) -> DepositMoneyUseCase:
    """Fornece instância do use case de depósito."""
    return DepositMoneyUseCase(repository, publisher)


async def get_withdraw_money_use_case(
    repository: Annotated[MongoAccountRepository, Depends(get_account_repository)],
    publisher: Annotated[RabbitMQEventPublisher, Depends(get_event_publisher)],
) -> WithdrawMoneyUseCase:
    """Fornece instância do use case de saque."""
    return WithdrawMoneyUseCase(repository, publisher)


async def get_transfer_money_use_case(
    repository: Annotated[MongoAccountRepository, Depends(get_account_repository)],
    publisher: Annotated[RabbitMQEventPublisher, Depends(get_event_publisher)],
) -> TransferMoneyUseCase:
    """Fornece instância do use case de transferência."""
    return TransferMoneyUseCase(repository, publisher)


# Type aliases para facilitar uso
AccountRepositoryDep = Annotated[MongoAccountRepository, Depends(get_account_repository)]
