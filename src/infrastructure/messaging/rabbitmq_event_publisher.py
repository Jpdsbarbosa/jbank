"""
Implementação do EventPublisher usando RabbitMQ.

aio-pika é um cliente assíncrono para RabbitMQ/AMQP.
"""

import json
from aio_pika import connect_robust, Message, ExchangeType
from aio_pika.abc import AbstractConnection, AbstractChannel, AbstractExchange

from ...domain.events import DomainEvent
from ...application.interfaces import EventPublisher


class RabbitMQEventPublisher(EventPublisher):
    """
    Publicador de eventos usando RabbitMQ.
    
    IMPLEMENTA a interface EventPublisher.
    """
    
    def __init__(self, rabbitmq_url: str, exchange_name: str) -> None:
        """
        Inicializa configuração do RabbitMQ.
        
        Args:
            rabbitmq_url: URL de conexão do RabbitMQ
            exchange_name: Nome do exchange
        """
        self.rabbitmq_url = rabbitmq_url
        self.exchange_name = exchange_name
        self.connection: AbstractConnection | None = None
        self.channel: AbstractChannel | None = None
        self.exchange: AbstractExchange | None = None
    
    async def connect(self) -> None:
        """
        Conecta ao RabbitMQ e cria exchange.
        
        IMPORTANTE: Deve ser chamado antes de publicar eventos!
        """
        # Conexão robusta (reconecta automaticamente se cair)
        self.connection = await connect_robust(self.rabbitmq_url)
        
        # Canal de comunicação
        self.channel = await self.connection.channel()
        
        # Exchange do tipo "topic" (permite routing complexo)
        self.exchange = await self.channel.declare_exchange(
            self.exchange_name,
            ExchangeType.TOPIC,  # Tipo: topic (permite padrões)
            durable=True,  # Persiste se RabbitMQ reiniciar
        )
    
    async def publish(self, event: DomainEvent) -> None:
        """
        Publica um evento no RabbitMQ.
        
        O evento é convertido para JSON e enviado para o exchange.
        """
        if not self.exchange:
            raise RuntimeError("Not connected to RabbitMQ. Call connect() first!")
        
        # Converte evento para dict
        event_dict = event.to_dict()
        
        # Serializa para JSON
        event_json = json.dumps(event_dict, default=str)
        
        # Cria mensagem
        message = Message(
            body=event_json.encode(),  # Body em bytes
            content_type="application/json",
            delivery_mode=2,  # Persistente (não perde se RabbitMQ cair)
        )
        
        # Routing key baseado no tipo do evento
        # Ex: "AccountCreated" -> routing key = "account.created"
        routing_key = self._get_routing_key(event.event_type)
        
        # Publica no exchange
        await self.exchange.publish(
            message,
            routing_key=routing_key,
        )
    
    async def publish_many(self, events: list[DomainEvent]) -> None:
        """Publica múltiplos eventos."""
        for event in events:
            await self.publish(event)
    
    def _get_routing_key(self, event_type: str) -> str:
        """
        Converte tipo do evento para routing key.
        
        AccountCreated -> account.created
        MoneyDeposited -> money.deposited
        TransferRequested -> transfer.requested
        """
        # Converte de PascalCase para snake_case
        # e adiciona pontos entre palavras
        import re
        snake_case = re.sub(r'(?<!^)(?=[A-Z])', '_', event_type).lower()
        return snake_case.replace('_', '.')
    
    async def close(self) -> None:
        """Fecha conexão com RabbitMQ."""
        if self.connection:
            await self.connection.close()