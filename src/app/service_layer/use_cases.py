from app.infrastructure.sqlalchemy import models
from app.service_layer import crud
from app.domain.entities.user import UserCreate
from app.domain.entities.wallet import WalletCreate, InsufficientFundsInTheAccount
from more_itertools import first_true
from sqlalchemy.orm import Session


def create_user_with_wallet(db: Session, user_in: UserCreate):
    user = crud.user.create(db, obj_in=user_in)
    crud.wallet.create(db, obj_in=WalletCreate(user_id=user.id))
    db.commit()
    db.refresh(user)

    return user


class DatabaseConsistencyIsBroken(Exception):
    pass


def transfer_payment_from_source_to_receiver(db: Session, *, wallet_id_source: int, wallet_id_receiver: int, amount: int):
    wallet_list = crud.wallet.get_by_ids_and_lock(db, ids=(wallet_id_source, wallet_id_receiver))

    if len(wallet_list) != 2:
        raise DatabaseConsistencyIsBroken

    wallet_source = first_true(wallet_list, pred=lambda x: x.id == wallet_id_source)
    wallet_receiver = first_true(wallet_list, pred=lambda x: x.id == wallet_id_receiver)

    if wallet_source.balance < amount:
        raise InsufficientFundsInTheAccount

    wallet_source.balance = models.Wallet.balance - amount
    wallet_receiver.balance = models.Wallet.balance + amount
    db.flush()

    # write history for source
    db.add(models.WalletHistory(
        wallet_id=wallet_source.id,
        user_id=wallet_source.user_id,
        balance=wallet_source.balance,
    ))

    # write history for receiver
    db.add(models.WalletHistory(
        wallet_id=wallet_receiver.id,
        user_id=wallet_receiver.user_id,
        balance=wallet_receiver.balance,
    ))

    db.commit()
    db.refresh(wallet_source)
    return wallet_source
