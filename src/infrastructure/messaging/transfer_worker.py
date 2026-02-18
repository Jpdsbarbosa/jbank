"""
Worker que processa transferências assincronamente.

Este worker escuta a fila de transferências no RabbitMQ,
processa cada transferência e publica o resultado.
"""

import json
import asyncio
from aio_pika import connect_robust, ExchangeType
from aio_pika.abc import AbstractIncomingMessage

from ...domain.value_objects import AccountNumber, Money
from ...domain.events import TransferCompleted, TransferFailed
from ..database.mongo_account_repository import MongoAccountRepository
from .rabbitmq_event_publisher import RabbitMQEventPublisher


class TransferWorker:
    """
    Worker que processa transferências da fila.
    
    Fluxo:
    1. Escuta fila "transfers"
    2. Recebe TransferRequested
    3. Busca contas no MongoDB
    4. Executa transferência (saque + depósito)
    5. Salva ambas as contas
    6. Publica TransferCompleted ou TransferFailed
    """
    
    def __init__(
        self,
        rabbitmq_url: str,
        mongodb_url: str,
        mongodb_database: str,
        exchange_name: str,
        queue_name: str,
    ) -> None:
        """
        Inicializa o worker.
        
        Args:
            rabbitmq_url: URL do RabbitMQ
            mongodb_url: URL do MongoDB
            mongodb_database: Nome do banco
            exchange_name: Nome do exchange
            queue_name: Nome da fila de transferências
        """
        self.rabbitmq_url = rabbitmq_url
        self.exchange_name = exchange_name
        self.queue_name = queue_name
        
        # Repositório para buscar/salvar contas
        self.repository = MongoAccountRepository(mongodb_url, mongodb_database)
        
        # Publisher para publicar eventos de resultado
        self.event_publisher = RabbitMQEventPublisher(rabbitmq_url, exchange_name)
    
    async def start(self) -> None:
        """
        Inicia o worker.
        
        Conecta ao RabbitMQ, declara fila e começa a processar mensagens.
        """
        print("🔄 Transfer Worker iniciando...")
        
        # Conecta ao RabbitMQ
        connection = await connect_robust(self.rabbitmq_url)
        channel = await connection.channel()
        
        # Declara exchange
        exchange = await channel.declare_exchange(
            self.exchange_name,
            ExchangeType.TOPIC,
            durable=True,
        )
        
        # Declara fila
        queue = await channel.declare_queue(
            self.queue_name,
            durable=True,  # Persiste se RabbitMQ reiniciar
        )
        
        # Bind fila ao exchange com routing key
        await queue.bind(exchange, routing_key="transfer.requested")
        
        # Conecta event publisher
        await self.event_publisher.connect()
        
        print(f"✅ Worker escutando fila '{self.queue_name}'...")
        print(f"✅ Aguardando eventos 'transfer.requested'...")
        
        # Começa a consumir mensagens
        await queue.consume(self._process_transfer)
        
        # Mantém rodando
        try:
            await asyncio.Future()  # Roda forever
        finally:
            await connection.close()
    
    async def _process_transfer(self, message: AbstractIncomingMessage) -> None:
        """
        Processa uma mensagem de transferência.
        
        Args:
            message: Mensagem do RabbitMQ
        """
        async with message.process():
            try:
                # Deserializa JSON
                event_data = json.loads(message.body.decode())
                
                print(f"\n📨 Processando transferência: {event_data['transfer_id']}")
                
                # Extrai dados
                transfer_id = event_data["transfer_id"]
                from_account_number = AccountNumber(value=event_data["from_account"])
                to_account_number = AccountNumber(value=event_data["to_account"])
                amount = Money.create(event_data["amount"])
                
                # Busca contas no MongoDB
                from_account = await self.repository.find_by_account_number(
                    from_account_number
                )
                to_account = await self.repository.find_by_account_number(
                    to_account_number
                )
                
                if not from_account:
                    raise ValueError(f"Conta origem {from_account_number} não encontrada")
                
                if not to_account:
                    raise ValueError(f"Conta destino {to_account_number} não encontrada")
                
                # Executa transferência
                # 1. Saca da conta origem (valida saldo automaticamente!)
                from_account.withdraw(amount)
                
                # 2. Deposita na conta destino
                to_account.deposit(amount)
                
                # 3. Salva ambas as contas
                await self.repository.save(from_account)
                await self.repository.save(to_account)
                
                # Publica evento de sucesso
                success_event = TransferCompleted(
                    transfer_id=transfer_id,
                    from_account=str(from_account_number),
                    to_account=str(to_account_number),
                    amount=str(amount.amount),
                )
                await self.event_publisher.publish(success_event)
                
                print(f"✅ Transferência {transfer_id} concluída com sucesso!")
                
            except Exception as e:
                # Algo deu errado!
                print(f"❌ Erro ao processar transferência: {e}")
                
                # Publica evento de falha
                failed_event = TransferFailed(
                    transfer_id=event_data.get("transfer_id", "unknown"),
                    from_account=event_data.get("from_account", ""),
                    to_account=event_data.get("to_account", ""),
                    amount=event_data.get("amount", "0"),
                    reason=str(e),
                )
                await self.event_publisher.publish(failed_event)
                
                print(f"❌ Transferência falhou: {e}")