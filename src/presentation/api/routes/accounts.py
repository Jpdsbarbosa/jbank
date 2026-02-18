"""Rotas de contas."""

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status

from src.application.use_cases import (
    CreateAccountUseCase,
    CreateAccountInput,
    DepositMoneyUseCase,
    DepositMoneyInput,
    WithdrawMoneyUseCase,
    WithdrawMoneyInput,
)
from src.infrastructure.database import MongoAccountRepository
from src.presentation.schemas import (
    CreateAccountRequest,
    AccountResponse,
    DepositRequest,
    WithdrawRequest,
    TransactionResponse,
)
from src.presentation.api.dependencies import (
    get_create_account_use_case,
    get_deposit_money_use_case,
    get_withdraw_money_use_case,
    get_account_repository,
)


router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.post("", response_model=AccountResponse, status_code=status.HTTP_201_CREATED)
async def create_account(
    request: CreateAccountRequest,
    use_case: Annotated[CreateAccountUseCase, Depends(get_create_account_use_case)],
):
    """
    Cria uma nova conta bancária.
    
    A conta é criada com status ANALYSIS (aguardando aprovação).
    """
    try:
        # Converte request para DTO do use case
        input_dto = CreateAccountInput(
            holder_name=request.holder_name,
            cpf=request.cpf,
            initial_balance=request.initial_balance,
        )
        
        # Executa use case
        output = await use_case.execute(input_dto)
        
        # Retorna response
        return AccountResponse(
            account_number=output.account_number,
            holder_name=output.holder_name,
            cpf=output.cpf,
            balance=output.balance,
            status=output.status,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/{account_number}/deposit", response_model=TransactionResponse)
async def deposit_money(
    account_number: str,
    request: DepositRequest,
    use_case: Annotated[DepositMoneyUseCase, Depends(get_deposit_money_use_case)],
):
    """Deposita dinheiro em uma conta."""
    try:
        input_dto = DepositMoneyInput(
            account_number=account_number,
            amount=request.amount,
        )
        
        output = await use_case.execute(input_dto)
        
        return TransactionResponse(
            account_number=output.account_number,
            old_balance=output.old_balance,
            amount=output.amount_deposited,
            new_balance=output.new_balance,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/{account_number}/withdraw", response_model=TransactionResponse)
async def withdraw_money(
    account_number: str,
    request: WithdrawRequest,
    use_case: Annotated[WithdrawMoneyUseCase, Depends(get_withdraw_money_use_case)],
):
    """Saca dinheiro de uma conta."""
    try:
        input_dto = WithdrawMoneyInput(
            account_number=account_number,
            amount=request.amount,
        )
        
        output = await use_case.execute(input_dto)
        
        return TransactionResponse(
            account_number=output.account_number,
            old_balance=output.old_balance,
            amount=output.amount_withdrawn,
            new_balance=output.new_balance,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/{account_number}/approve", status_code=status.HTTP_200_OK)
async def approve_account(
    account_number: str,
    use_case: Annotated[MongoAccountRepository, Depends(get_account_repository)],
):
    """Aprova uma conta (muda status para ACTIVE)."""
    try:
        from src.domain.value_objects import AccountNumber
        
        acc_num = AccountNumber(value=account_number)
        account = await use_case.find_by_account_number(acc_num)
        
        if not account:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conta não encontrada")
        
        account.approve()
        await use_case.save(account)
        
        return {"message": f"Conta {account_number} aprovada com sucesso!"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
