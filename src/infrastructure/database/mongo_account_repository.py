"""
Implementação do AccountRepository usando MongoDB.

Motor é o driver assíncrono oficial do MongoDB para Python.
"""

from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection

from ...domain.entities import Account, AccountStatus
from ...domain.value_objects import AccountNumber, CPF, Money
from ...application.interfaces import AccountRepository


class MongoAccountRepository(AccountRepository):
    """
    Repositório de contas usando MongoDB.
    
    IMPLEMENTA a interface AccountRepository.
    """
    
    def __init__(self, mongodb_url: str, database_name: str) -> None:
        """
        Inicializa conexão com MongoDB.
        
        Args:
            mongodb_url: URL de conexão do MongoDB
            database_name: Nome do banco de dados
        """
        self.client = AsyncIOMotorClient(mongodb_url)
        self.database = self.client[database_name]
        self.collection: AsyncIOMotorCollection = self.database["accounts"]
    
    async def save(self, account: Account) -> None:
        """
        Salva ou atualiza uma conta no MongoDB.
        
        Usa upsert (update + insert):
        - Se existir: atualiza
        - Se não existir: insere
        """
        # Converte Account (entidade) para dict (MongoDB)
        account_dict = {
            "account_number": str(account.account_number),
            "holder_name": account.holder_name,
            "cpf": str(account.cpf),
            "balance": str(account.balance.amount),
            "status": account.status.value,
            "created_at": account.created_at,
            "updated_at": account.updated_at,
        }
        
        # Upsert: atualiza se existe, insere se não existe
        await self.collection.update_one(
            {"account_number": account_dict["account_number"]},  # Filtro
            {"$set": account_dict},  # Dados
            upsert=True  # Cria se não existir
        )
    
    async def find_by_account_number(
        self, 
        account_number: AccountNumber
    ) -> Optional[Account]:
        """
        Busca uma conta pelo número.
        
        Query MongoDB: db.accounts.findOne({account_number: "ACC-..."})
        """
        document = await self.collection.find_one(
            {"account_number": str(account_number)}
        )
        
        if not document:
            return None
        
        # Converte dict (MongoDB) para Account (entidade)
        return self._document_to_account(document)
    
    async def find_by_cpf(self, cpf: CPF) -> Optional[Account]:
        """
        Busca uma conta pelo CPF.
        
        Query MongoDB: db.accounts.findOne({cpf: "12345678900"})
        """
        document = await self.collection.find_one(
            {"cpf": str(cpf)}
        )
        
        if not document:
            return None
        
        return self._document_to_account(document)
    
    async def exists_by_cpf(self, cpf: CPF) -> bool:
        """
        Verifica se existe conta com este CPF.
        
        Query MongoDB: db.accounts.countDocuments({cpf: "..."}) > 0
        """
        count = await self.collection.count_documents(
            {"cpf": str(cpf)}
        )
        return count > 0
    
    async def delete(self, account_number: AccountNumber) -> None:
        """
        Remove uma conta (ou soft delete).
        
        Query MongoDB: db.accounts.deleteOne({account_number: "..."})
        """
        await self.collection.delete_one(
            {"account_number": str(account_number)}
        )
    
    def _document_to_account(self, document: dict) -> Account:
        """
        Converte documento MongoDB para entidade Account.
        
        Helper method privado.
        """
        return Account(
            account_number=AccountNumber(value=document["account_number"]),
            holder_name=document["holder_name"],
            cpf=CPF(document["cpf"]),
            balance=Money.create(document["balance"]),
            status=AccountStatus(document["status"]),
            created_at=document["created_at"],
            updated_at=document["updated_at"],
        )
    
    async def close(self) -> None:
        """Fecha conexão com MongoDB."""
        self.client.close()