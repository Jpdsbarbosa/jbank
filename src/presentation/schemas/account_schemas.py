"""
Schemas Pydantic para requisições/respostas da API.

DTOs (Data Transfer Objects) que definem o formato JSON.
"""

from pydantic import BaseModel, Field
from datetime import datetime


# ==================== ACCOUNT SCHEMAS ====================

class CreateAccountRequest(BaseModel):
    """Schema para criar conta."""
    holder_name: str = Field(..., min_length=3, max_length=100)
    cpf: str = Field(..., min_length=11, max_length=14)
    initial_balance: float = Field(..., ge=0)
    
    class Config:
        json_schema_extra = {
            "example": {
                "holder_name": "João Paulo",
                "cpf": "12345678909",
                "initial_balance": 1000.00
            }
        }


class AccountResponse(BaseModel):
    """Schema de resposta com dados da conta."""
    account_number: str
    holder_name: str
    cpf: str
    balance: str
    status: str
    created_at: datetime | None = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "account_number": "ACC-550e8400-e29b-41d4-a716-446655440000",
                "holder_name": "João Paulo",
                "cpf": "12345678909",
                "balance": "1000.00",
                "status": "analysis",
                "created_at": "2024-02-08T10:30:00"
            }
        }


class DepositRequest(BaseModel):
    """Schema para depósito."""
    amount: float = Field(..., gt=0)
    
    class Config:
        json_schema_extra = {
            "example": {
                "amount": 500.00
            }
        }


class WithdrawRequest(BaseModel):
    """Schema para saque."""
    amount: float = Field(..., gt=0)
    
    class Config:
        json_schema_extra = {
            "example": {
                "amount": 200.00
            }
        }


class TransactionResponse(BaseModel):
    """Schema de resposta de transação."""
    account_number: str
    old_balance: str
    amount: str
    new_balance: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "account_number": "ACC-550e8400-e29b-41d4-a716-446655440000",
                "old_balance": "1000.00",
                "amount": "500.00",
                "new_balance": "1500.00"
            }
        }
