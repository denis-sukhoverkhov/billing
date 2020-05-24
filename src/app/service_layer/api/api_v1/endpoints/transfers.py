from typing import Any

from app.domain import entities
from app.domain.entities.wallet import InsufficientFundsInTheAccount
from app.service_layer.api import deps
from app.service_layer.use_cases import DatabaseConsistencyIsBroken, transfer_payment_from_source_to_receiver
from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

router = APIRouter()


@router.post("/from/{wallet_id_source}/to/{wallet_id_receiver}",
             response_model=entities.Wallet, status_code=status.HTTP_200_OK)
def payment_transfer_from_source_wallet_to_receiver_wallet(
        *,
        db: Session = Depends(deps.get_db),
        wallet_id_source: int,
        wallet_id_receiver: int,
        amount: int = Body(..., gt=0, embed=True),
) -> Any:
    if wallet_id_source == wallet_id_receiver:
        raise HTTPException(
            status_code=400,
            detail="wallet_id_source and wallet_id_receiver are equals.",
        )

    try:
        return transfer_payment_from_source_to_receiver(
            db, wallet_id_source=wallet_id_source, wallet_id_receiver=wallet_id_receiver, amount=amount)
    except DatabaseConsistencyIsBroken:
        raise HTTPException(
            status_code=500,
            detail="Something was wrong",
        )
    except InsufficientFundsInTheAccount:
        raise HTTPException(
            status_code=400,
            detail="Insufficient funds in the account.",
        )
