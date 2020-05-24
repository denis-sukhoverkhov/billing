from typing import Optional

from app.domain.entities.wallet import WalletCreate, WalletUpdate
from app.infrastructure.sqlalchemy import models
from app.service_layer.crud.base import CRUDBase
from sqlalchemy.orm import Session


class CRUDWalletHistory(CRUDBase[models.WalletHistory, WalletCreate, WalletUpdate]):
    def get_by(self, db: Session, *, wallet_id: int) -> Optional[models.WalletHistory]:
        return db.query(models.WalletHistory).filter(models.WalletHistory.wallet_id == wallet_id).all()


wallet_history = CRUDWalletHistory(models.WalletHistory)
