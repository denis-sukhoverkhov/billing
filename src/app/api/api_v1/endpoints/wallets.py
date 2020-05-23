from typing import Any

from app import crud
from app.api import deps
from app.domain import entities
from app.infrastructure.sqlalchemy import models
from fastapi import APIRouter, Depends, Body, HTTPException
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/{wallet_id}/enroll", response_model=entities.Wallet)
def enroll_cash_to_wallet(
    *,
    db: Session = Depends(deps.get_db),
    wallet_id: int,
    amount: int = Body(..., gt=0, embed=True),
) -> Any:
    wallet = crud.wallet.get_by_pk(db, pk=wallet_id)
    if not wallet:
        raise HTTPException(
            status_code=400,
            detail="The wallet with this id not exists.",
        )

    wallet.balance = models.Wallet.balance + amount
    db.commit()
    db.refresh(wallet)
    return wallet
