from typing import Iterable, Optional

from app.infrastructure.sqlalchemy import models
from app.service_layer.crud.base import CRUDBase
from app.domain.entities.wallet import WalletCreate, WalletUpdate, WalletNotFound
from sqlalchemy.orm import Session


class CRUDWallet(CRUDBase[models.Wallet, WalletCreate, WalletUpdate]):
    def get_by_pk(self, db: Session, *, pk: int) -> Optional[models.Wallet]:
        return db.query(models.Wallet).filter(models.Wallet.id == pk).first()

    def get_by_ids_and_lock(self, db: Session, *, ids: Iterable[int]) -> Optional[models.Wallet]:
        return db.query(models.Wallet).filter(models.Wallet.id.in_(ids)).with_for_update().all()

    def create(self, db: Session, *, obj_in: WalletCreate) -> models.Wallet:
        db.begin(subtransactions=True)
        db_obj = models.Wallet(
            user_id=obj_in.user_id,
        )
        db.add(db_obj)
        db.flush()

        # write history
        db.add(models.WalletHistory(
            wallet_id=db_obj.id,
            user_id=db_obj.user_id,
            balance=db_obj.balance,
        ))

        db.commit()
        db.refresh(db_obj)
        return db_obj

    def atomic_enroll_balance(self, db: Session, *, obj_id: int, amount: int) -> models.Wallet:
        obj = self.get_by_pk(db, pk=obj_id)
        if not obj:
            raise WalletNotFound

        obj.balance = models.Wallet.balance + amount
        db.flush()

        # write history
        db.add(models.WalletHistory(
            wallet_id=obj.id,
            user_id=obj.user_id,
            balance=obj.balance,
        ))

        db.commit()
        db.refresh(obj)

        return obj


wallet = CRUDWallet(models.Wallet)
