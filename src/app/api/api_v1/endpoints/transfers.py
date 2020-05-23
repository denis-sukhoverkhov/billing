from typing import Any

from app import crud
from app.api import deps
from app.domain import entities
from app.infrastructure.sqlalchemy import models
from fastapi import APIRouter, Body, Depends, HTTPException
from more_itertools import first_true
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/from/{wallet_id_source}/to/{wallet_id_receiver}", response_model=entities.Wallet)
def payment_transfer_from_wallet_to_wallet(
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

    wallet_list = crud.wallet.get_by_ids_and_lock(db, ids=(wallet_id_source, wallet_id_receiver))
    if len(wallet_list) != 2:
        raise HTTPException(
            status_code=500,
            detail="Something was wrong",
        )

    wallet_source = first_true(wallet_list, pred=lambda x: x.id == wallet_id_source)
    wallet_receiver = first_true(wallet_list, pred=lambda x: x.id == wallet_id_receiver)

    if wallet_source.balance < amount:
        raise HTTPException(
            status_code=400,
            detail="Insufficient funds in the account.",
        )

    wallet_source.balance = models.Wallet.balance - amount
    wallet_receiver.balance = models.Wallet.balance + amount
    db.commit()
    db.refresh(wallet_receiver)
    return wallet_receiver
