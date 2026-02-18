"""Rotas de transferências."""

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status

from src.application.use_cases import (
    TransferMoneyUseCase,
    TransferMoneyInput,
)
from src.presentation.schemas import TransferRequest, TransferResponse
from src.presentation.api.dependencies import get_transfer_money_use_case


router = APIRouter(prefix="/transfers", tags=["transfers"])


@router.post("", response_model=TransferResponse, status_code=status.HTTP_202_ACCEPTED)
async def transfer_money(
    request: TransferRequest,
    use_case: Annotated[TransferMoneyUseCase, Depends(get_transfer_money_use_case)],
):
    """
    Solicita uma transferência entre contas.
    
    A transferência é processada de forma ASSÍNCRONA.
    Retorna status 202 (Accepted) e status "pending".
    """
    try:
        input_dto = TransferMoneyInput(
            from_account_number=request.from_account_number,
            to_account_number=request.to_account_number,
            amount=request.amount,
        )
        
        output = await use_case.execute(input_dto)
        
        return TransferResponse(
            transfer_id=output.transfer_id,
            from_account=output.from_account,
            to_account=output.to_account,
            amount=output.amount,
            status=output.status,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
