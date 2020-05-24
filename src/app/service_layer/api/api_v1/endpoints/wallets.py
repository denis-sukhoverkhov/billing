from typing import Any

from app.domain import entities
from app.domain.entities.wallet import WalletNotFound
from app.service_layer import crud
from app.service_layer.api import deps
from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

router = APIRouter()


@router.post("/{wallet_id}/enroll", response_model=entities.Wallet, status_code=status.HTTP_200_OK)
def enroll_cash_to_wallet(
    *,
    db: Session = Depends(deps.get_db),
    wallet_id: int,
    amount: int = Body(..., gt=0, embed=True),
) -> Any:
    try:
        return crud.wallet.atomic_enroll_balance(db, obj_id=wallet_id, amount=amount)
    except WalletNotFound:
        raise HTTPException(
            status_code=400,
            detail="The wallet with this id not exists.",
        )
