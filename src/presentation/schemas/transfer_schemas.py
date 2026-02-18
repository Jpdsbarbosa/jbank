"""Schemas para transferências."""

from pydantic import BaseModel, Field


class TransferRequest(BaseModel):
    """Schema para solicitar transferência."""
    from_account_number: str
    to_account_number: str
    amount: float = Field(..., gt=0)
    
    class Config:
        json_schema_extra = {
            "example": {
                "from_account_number": "ACC-550e8400-e29b-41d4-a716-446655440000",
                "to_account_number": "ACC-660e8400-e29b-41d4-a716-446655440000",
                "amount": 150.00
            }
        }


class TransferResponse(BaseModel):
    """Schema de resposta de transferência."""
    transfer_id: str
    from_account: str
    to_account: str
    amount: str
    status: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "transfer_id": "770e8400-e29b-41d4-a716-446655440000",
                "from_account": "ACC-550e8400-e29b-41d4-a716-446655440000",
                "to_account": "ACC-660e8400-e29b-41d4-a716-446655440000",
                "amount": "150.00",
                "status": "pending"
            }
        }
