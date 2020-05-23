from typing import Iterable, Optional

from app.crud.base import CRUDBase
from app.domain.entities.wallet import WalletCreate, WalletUpdate
from app.infrastructure.sqlalchemy.models.wallet import Wallet
from sqlalchemy.orm import Session


class CRUDWallet(CRUDBase[Wallet, WalletCreate, WalletUpdate]):
    def get_by_pk(self, db: Session, *, pk: int) -> Optional[Wallet]:
        return db.query(Wallet).filter(Wallet.id == pk).first()

    def get_by_ids_and_lock(self, db: Session, *, ids: Iterable[int]) -> Optional[Wallet]:
        return db.query(Wallet).filter(Wallet.id.in_(ids)).with_for_update().all()

    def create(self, db: Session, *, obj_in: WalletCreate) -> Wallet:
        db.begin(subtransactions=True)
        db_obj = Wallet(
            user_id=obj_in.user_id,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    # def update(
    #     self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    # ) -> User:
    #     if isinstance(obj_in, dict):
    #         update_data = obj_in
    #     else:
    #         update_data = obj_in.dict(exclude_unset=True)
    #     if update_data["password"]:
    #         hashed_password = get_password_hash(update_data["password"])
    #         del update_data["password"]
    #         update_data["hashed_password"] = hashed_password
    #     return super().update(db, db_obj=db_obj, obj_in=update_data)
    #
    # def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
    #     user = self.get_by_email(db, email=email)
    #     if not user:
    #         return None
    #     if not verify_password(password, user.hashed_password):
    #         return None
    #     return user
    #
    # def is_active(self, user: User) -> bool:
    #     return user.is_active

    # def is_superuser(self, user: User) -> bool:
    #     return user.is_superuser


wallet = CRUDWallet(Wallet)
