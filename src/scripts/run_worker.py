"""
Script para rodar o Transfer Worker.

Executa: python -m src.scripts.run_worker
"""

import asyncio
from src.infrastructure.config import settings
from src.infrastructure.messaging import TransferWorker


async def main():
    """Inicia o worker de transferências."""
    worker = TransferWorker(
        rabbitmq_url=settings.rabbitmq_url,
        mongodb_url=settings.mongodb_url,
        mongodb_database=settings.mongodb_database,
        exchange_name=settings.rabbitmq_exchange,
        queue_name=settings.rabbitmq_transfer_queue,
    )
    
    await worker.start()


if __name__ == "__main__":
    asyncio.run(main())
